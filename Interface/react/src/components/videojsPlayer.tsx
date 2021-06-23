/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React, { useRef, useEffect, useContext } from 'react'
import videojs from 'video.js'
import 'video.js/dist/video-js.css'
import 'bootstrap-icons/font/bootstrap-icons.css'

import { Box, size } from 'classes/box'
import { environmentContext } from './environmentContext'
import { authContext } from './authContext'

/** Properties for the VideoPlayer component, including all callbacks that can be called with the player buttons,
 * as well as default videojs properties. */
export type VideoPlayerProps = {
  setSnapCallback: (snap: (box: Box) => string | undefined) => void // Callback to set snap functionality.
  onTimestamp: (time: number) => void // Callback which updates the timestamp for the overlay.
  onPlayPause: (playing: boolean) => void // Callback which updates the playback state for the overlay.
  onPrimary: () => void // Callback to make this videoplayer the primary video player.
  onResize?: (size: size) => void // Callback to update viewport on resize.
} & videojs.PlayerOptions

/**
 * Wrapper for a videojs player that adds custom functionality and syncing with bounding boxes.
 * @param props The properties for the VideoPlayer.
 * @returns A videojs player injected with custom functionality.
 */
export function VideoPlayer(props: VideoPlayerProps) {
  // Authentication hooks.
  const { status, token } = useContext(authContext)

  // The DOM node to attach the videoplayer to.
  const videoRef = useRef<HTMLVideoElement>(null)

  // The videoplayer object.
  const playerRef = useRef<videojs.Player>()

  // Use the snap function callback to give the parent the ability to create snaps.
  useEffect(() => {
    props.setSnapCallback(takeSnapshot)
  }, [props.setSnapCallback])

  // Constants used to calculate the timestamp of the livestream based on segment file names.
  const initialUriIntervalRef = useRef<number>() // How often to check for the initial segment name.
  const changeIntervalRef = useRef<number>() // How often to check for a new segemnt after the inital has been obtained.
  const updateIntervalRef = useRef<number>() // How often to update the timestamp once it's known.

  const { bufferTime, segmentLength } = useContext(environmentContext)

  var startUri // The name of the first segment received by the videoplayer.
  var startTime // The timestamp of the stream where the player was started.
  var timeStamp // The current timestamp of the stream.
  var playerSwitchTime // The timestamp of when the video player switch to the second segment.
  var playerStartTime // The current time of the video player when it's first being played.
  var bufferTimer // The interval that counts down while buffering.

  useEffect(() => {
    // Add a token query parameter to the src, this will be used for the index file but not in subsequent requests.
    if (props.sources?.[0].src && status != 'no-auth')
      props.sources[0].src += `?Bearer=${token}`

    // Instantiate videojs. Ignore the videojs constructor, as this would otherwise throw error during documentation generation.
    //@ts-ignore
    playerRef.current = videojs(videoRef.current, props, () => {
      var player = playerRef.current

      // If the user is authenticated, add xhr headers with the bearer token to authorize.
      if (status == 'authenticated') {
        //@ts-ignore
        videojs.Vhs.xhr.beforeRequest = function (options) {
          // As headers might not exist yet, create them if not.
          options.headers = options.headers || {}
          options.headers.Authorization = `Bearer ${token}`
          return options
        }
      }

      // Add button to make this videoplayer the primary player at the top of the page.
      player?.controlBar.addChild(
        new extraButton(player, {
          onPress: props.onPrimary,
          icon: 'bi-zoom-in',
          text: 'Set primary'
        }),
        {},
        0
      )

      player?.on('playerresize', () => onResize())
      player?.on('play', () => onResize())
      player?.on('loadeddata', () => onResize())

      /* Timestamp calculation.
       * On the first time a stream is started, attempt getting the segment name, keep going until a name is obtained. */
      player?.on('firstplay', () => {
        playerStartTime = playerRef.current?.currentTime()
        initialUriIntervalRef.current = player?.setInterval(() => {
          getInitialUri()
        }, 200)
      })

      // Every time the videoplayer is resumed, go back to updating the timestamp.
      player?.on('play', () => {
        updateIntervalRef.current = player?.setInterval(() => {
          updateTimestamp()
        }, 100)
        props.onPlayPause(true)
      })

      /* Every time the player is paused, stop the manual timestamp update.
       * The player.currentTime() method from videoJS will keep going in the background.
       * If the manual update isn't stopped it will think the time while paused is double. */
      player?.on('pause', () => {
        if (updateIntervalRef.current)
          player?.clearInterval(updateIntervalRef.current)
        props.onPlayPause(false)
      })

      // When the player starts bufferring it fires the waiting event.
      player?.on('waiting', () => {
        if (!startTime) return // Prevent inconsistencies on firstplay when there is no timestamp yet.

        // Waiting may happen twice in a row, so prevent multiple timers.
        if (!bufferTimer) {
          var bufferTimeVar = bufferTime // How long to wait for.
          const delta = 0.5 // Update frequency, every <delta> seconds it checks the status.

          // The interval will count down and show the alert if the countdown reaches 0.
          bufferTimer = player?.setInterval(() => {
            bufferTimeVar -= delta
            if (bufferTimeVar <= 0) {
              // Clear the interval and automatically reload the player
              player?.clearInterval(bufferTimer)
              bufferTimer = undefined
              player?.pause()

              if (props.sources && props.sources[0].type)
                player?.src({
                  src: props.sources[0].src,
                  type: props.sources[0].type
                })
              else if (props.sources) player?.src({ src: props.sources[0].src })

              startTime = undefined
              player?.load()
              player?.play()
            }
          }, delta * 1000)
        }
      })

      /* Seeked is fired when the player starts/resumes playing video.
       * Use this as a signal to stop waiting for a buffer if the timer is running. */
      player?.on('seeked', () => {
        if (bufferTimer) {
          player?.clearInterval(bufferTimer)
          bufferTimer = undefined
        }
      })
    })

    return () => playerRef.current?.dispose()
  }, [])

  /**
   * Accesses the video player tech.
   * @returns URI from the first segment in the playlist.
   */
  function getURI(): string | undefined {
    // Passing any argument suppresses a warning about accessing the tech.
    return playerRef.current?.tech({ randomArg: true })?.textTracks()?.[0]
      ?.activeCues?.[0]?.['value']?.uri
  }

  /**
   * Used in an interval, attempts to get an URI and once it has one cancels itself,
   * and starts a new interval that waits for a change in URI.
   */
  function getInitialUri() {
    // Attempt to get the segment name.
    let currentUri = getURI()
    if (currentUri) {
      // If a segment name has been found, save it and start looking for an updated name.
      startUri = currentUri
      if (initialUriIntervalRef.current)
        playerRef.current?.clearInterval(initialUriIntervalRef.current)
      changeIntervalRef.current = playerRef.current?.setInterval(() => {
        lookForUriUpdate()
      }, 1000 / 24)
    }
  }

  /**
   * Used in an interval, attempts to get the URI of the current segment, and compares this to the initial URI.
   * If it is not the same, cancels the interval and sets the time that the timestamp will be based on.
   */
  function lookForUriUpdate() {
    let currentUri = getURI()
    if (currentUri !== startUri) {
      // Ensure it is a string because typescript.
      if (typeof currentUri === 'string') {
        playerSwitchTime = playerRef.current?.currentTime()
        console.log('URI changed: ', currentUri)
        startTime = GetSegmentStarttime(currentUri, segmentLength)
        console.log('Starttime: ', PrintTimestamp(startTime))
        if (changeIntervalRef.current)
          playerRef.current?.clearInterval(changeIntervalRef.current)
      }
    }
  }

  /**
   * Should be done in an interval, started whenever the user hits play.
   * This interval should be stopped whenever the user pauses.
   */
  function updateTimestamp() {
    if (!startTime) {
      return
    }

    let currentPlayer = playerRef.current?.currentTime()
    timeStamp = startTime + currentPlayer - playerSwitchTime + 0.2

    // Update timestamp for overlay.
    props.onTimestamp(timeStamp)
  }

  /** Calls the onResize callback function in order to let the overlay know the exact screen dimensions to scale to. */
  function onResize() {
    if (playerRef.current && props.onResize) {
      // Get the dimensions of the video player.
      var player = playerRef.current.currentDimensions()

      var playerWidth = player.width
      var playerHeight = player.height
      var playerAspect = playerWidth / playerHeight

      var videoWidth = playerRef.current.videoWidth()
      var videoHeight = playerRef.current.videoHeight()
      var videoAspect = videoWidth / videoHeight

      // If video aspect can't be gotten, use default 16:9.
      if (isNaN(videoAspect)) {
        videoAspect = 16 / 9
        // Set the video width to match ratio.
        if (playerAspect < videoAspect) {
          videoWidth = playerWidth
          videoHeight = (playerWidth / 16) * 9
        } else {
          videoWidth = (playerHeight / 9) * 16
          videoHeight = playerHeight
        }
      }

      // Stretch video to match width.
      if (playerAspect < videoAspect) {
        var widthRatio = playerWidth / videoWidth
        var actualVideoHeight = widthRatio * videoHeight
        props.onResize({
          width: playerWidth,
          height: actualVideoHeight,
          left: 0,
          top: (playerHeight - actualVideoHeight) / 2
        })
        // Stretch video to match height.
      } else {
        var heightRatio = playerHeight / videoHeight
        var actualVideoWidth = heightRatio * videoWidth
        props.onResize({
          width: actualVideoWidth,
          height: playerHeight,
          left: (playerWidth - actualVideoWidth) / 2,
          top: 0
        })
      }
    }
  }

  /**
   * Create an image from a selected box.
   * @param box The box from which the cutout should be generated.
   * @returns A Data-URL encoded image string.
   */
  function takeSnapshot(box: Box) {
    if (videoRef.current) {
      // Create size relative to videoplayer.
      var { left, top, width, height } = box.toSize(
        videoRef.current.videoWidth,
        videoRef.current.videoHeight
      )
      // Create new canvas of correct size.
      var canvas = document.createElement('canvas')
      canvas.width = width
      canvas.height = height
      var context = canvas.getContext('2d')
      if (context) {
        // Create the cutout from the video
        context.drawImage(
          videoRef.current,
          left,
          top,
          width,
          height,
          0,
          0,
          width,
          height
        )
        return canvas.toDataURL()
      }
    }
  }

  /* Wrap the player in a div with a `data-vjs-player` attribute so videojs won't create additional wrapper in the DOM.
   * See https://github.com/videojs/video.js/pull/3856 */
  return (
    <div
      data-testid='videojsplayer'
      className='c-player'
      style={{ width: '100%', height: '100%' }}
    >
      <div
        className='c-player__screen vjs-fill'
        data-vjs-player='true'
        style={{ width: '100%', height: '100%' }}
      >
        <video ref={videoRef} className='video-js' />
      </div>
    </div>
  )
}

/**
 * Create an additional button on the control bar.
 * See: https://stackoverflow.com/questions/35604358/videojs-v5-adding-custom-components-in-es6-am-i-doing-it-right
 */
export type ToggleSizeButtonOptions = {
  onPress: () => void
  icon: string
  text: string
}

/** Add a custom button to the videojs player. */
class extraButton extends videojs.getComponent('Button') {
  private onClick: () => void

  constructor(player, options: ToggleSizeButtonOptions) {
    super(player, {})
    this.controlText(options.text)
    this.onClick = options.onPress
    this.addClass(options.icon)
  }

  public handleClick(_e) {
    this.onClick()
  }
}

/**
 * Takes a timestamp in seconds and converts it to a string with the format mm:ss:ms.
 * @param time The time in seconds.
 * @returns The time formatted as mm:ss.
 */
export function PrintTimestamp(time: number): string {
  let min = Math.floor(time / 60)
  // Rounded to one decimal.
  let sec = (time % 60).toFixed(1)
  // Universify amount of numbers.
  if (parseFloat(sec) < 10) sec = '0' + sec
  return min + ':' + sec
}

/**
 * Takes the filename of a segment of the stream and determines the time of the video when this segment started.
 * @param segName The filename of the segment.
 * @returns The time in seconds.
 */
export function GetSegmentStarttime(
  segName: string,
  segmentLength: number
): number {
  // Assuming the forwarder will always send a stream using.
  // HLS, which gives .ts files.
  if (!segName.endsWith('.ts')) {
    console.warn(
      'GetSegmentStarttime: expected .ts file but got something else'
    )
    return NaN
  }

  // Filename should contain '_V' if it comes from the forwarder.
  if (segName.indexOf('_V') === -1) {
    console.warn('Video file not from forwarder')
    return NaN
  }

  // Filename ends with _VXYYY.ts where X is a version and YYY is the segment number.
  let end = segName.split('_V')[1]
  let number = end.slice(1, end.length - 3) // Remove the X and the .ts.
  // The segments have a certain length, so multiply the number with the length for the time.
  return (parseInt(number) - 1) * segmentLength
}
