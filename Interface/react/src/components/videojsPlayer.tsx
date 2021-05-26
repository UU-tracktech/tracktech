/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

/*
  This component creates a videoplayer using the VideoJS plugin
*/

import React from 'react'
import videojs from 'video.js'
import 'video.js/dist/video-js.css'
import 'bootstrap-icons/font/bootstrap-icons.css'

/** The properties used by the videoplayer */
export type VideoPlayerProps = {
  onTimestamp: (time: number) => void //Callback which updates the timestamp for the overlay
  onPlayPause: (playing: boolean) => void //Callback which updates the playback state for the overlay
  onPrimary: () => void //Callback to make this videoplayer the primary video player
  onResize?: (width: number, height: number, left: number, top: number) => void //Callback to update viewport on resize
} & videojs.PlayerOptions

export function VideoPlayer(props: VideoPlayerProps) {
  /** The DOM node to attach the videplayer to */
  var videoNode: HTMLVideoElement

  /** The videoplayer object */
  const playerRef = React.useRef<videojs.Player>()

  //Constants used to calculate the timestamp of the livestream based on segment file names
  const initialUriIntervalRef = React.useRef<number>() //How often to check for the initial segment name
  const changeIntervalRef = React.useRef<number>() //how often to check for a new segemnt after the inital has been obtained
  const updateIntervalRef = React.useRef<number>() //How often to update the timestamp once it's known

  var startUri //The name of the first segment received by the videoplayer
  var startTime //The timestamp of the stream where the player was started
  var timeStamp //The current timestamp of the stream
  var playerSwitchTime //The timestamp of when the video player switch to the second segment
  var playerStartTime //The current time of the video player when it's first being played

  React.useEffect(() => {
    // instantiate video.js
    playerRef.current = videojs(videoNode, props, () => {
      var player = playerRef.current

      //Add button to make this videoplayer the primary player at the top of the page
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

      //Timestamp calculation
      /* On the first time a stream is started, attempt getting the
         segment name, keep going until a name is obtained */
      player?.on('firstplay', () => {
        playerStartTime = playerRef.current?.currentTime()
        initialUriIntervalRef.current = player?.setInterval(() => {
          getInitialUri()
        }, 200)
      })

      //Every time the videoplayer is unpaused, go back to updating the timestamp
      player?.on('play', () => {
        updateIntervalRef.current = player?.setInterval(() => {
          updateTimestamp()
        }, 100)
        props.onPlayPause(true)
      })

      //Every time the player is paused, stop our manual timestamp update
      //The player.currentTime() method from videoJS will keep going in the background
      //If we don't stop our own update it will think the time while paused is double
      player?.on('pause', () => {
        if (updateIntervalRef.current)
          player?.clearInterval(updateIntervalRef.current)
        props.onPlayPause(false)
      })

      player?.on('seeked', () => {
        //reached a timestamp and starts to play
        //Seems to always happen after a waiting
        console.log('Event: seeked')
      })
      player?.on('waiting', () => {
        //Seems to happen on buffer
        console.log('Event: waiting')
      })
    })

    return () => playerRef.current?.dispose()
  }, [])

  /**
   * Accesses the video player tech and returns the URI
   * from the first segment in the playlist
   */
  function getURI(): string | undefined {
    try {
      //passing any argument suppresses a warning about accessing the tech
      let tech = playerRef.current?.tech({ randomArg: true })
      if (tech) {
        //ensure that the current playing segment has a uri
        if (tech.textTracks()[0].activeCues[0]['value'].uri) {
          //console.log('value:', tech.textTracks()[0].activeCues[0]['value'].uri)
          return tech.textTracks()[0].activeCues[0]['value'].uri
        }
      }
    } catch (e) {
      console.warn(e)
      return undefined
    }
  }

  /**
   * Used in an interval, attempts to get an URI and
   * once it has one cancels itself, and starts a new
   * interval that waits for a change in URI
   */
  function getInitialUri() {
    //attempt to get the segment name
    let currentUri = getURI()
    if (currentUri) {
      //if a segment name has been found, save it and start looking for an updated name
      //console.log('InitialURI: ', currentUri)

      startUri = currentUri
      if (initialUriIntervalRef.current)
        playerRef.current?.clearInterval(initialUriIntervalRef.current)
      changeIntervalRef.current = playerRef.current?.setInterval(() => {
        lookForUriUpdate()
      }, 1000 / 24)
    }
  }

  /**
   * Used in an interval, attempts to get the URI of the current
   * segment, and compares this to the initial URI. If it is not
   * the same, cancels the interval and sets the time that
   * the timestamp will be based on
   */
  function lookForUriUpdate() {
    let currentUri = getURI()
    if (currentUri !== startUri) {
      //ensure it is a string because typescript
      if (typeof currentUri === 'string') {
        playerSwitchTime = playerRef.current?.currentTime()
        console.log('URI changed: ', currentUri)
        startTime = GetSegmentStarttime(currentUri)
        console.log('Starttime: ', PrintTimestamp(startTime))
        playerRef.current?.currentTime(playerStartTime)
        if (changeIntervalRef.current)
          playerRef.current?.clearInterval(changeIntervalRef.current)
      }
    }
  }

  /**
   * Should be done in an interval, started whenever the user hits play
   * this interval should be stopped whenever the user pauses
   */
  function updateTimestamp() {
    if (!startTime) {
      //console.log('Timestamp: Loading...')
      return
    }

    let currentPlayer = playerRef.current?.currentTime()
    timeStamp = startTime + currentPlayer - playerSwitchTime + 0.2

    //Update timestamp for overlay
    props.onTimestamp(timeStamp)

    //print this videoplayer info to console as 1 object
    // let toPrint = {
    //   timeStamp: PrintTimestamp(timeStamp),
    //   frameID: timeStamp,
    // }
    //console.log(toPrint)
  }

  /**
   * Calls the onResize callback function in order to let the overlay know the exact screen dimensions to scale to
   */
  function onResize() {
    if (playerRef.current && props.onResize) {
      var player = playerRef.current.currentDimensions()

      var playerWidth = player.width
      var playerHeight = player.height
      var playerAspect = playerWidth / playerHeight

      var videoWidth = playerRef.current.videoWidth()
      var videoHeight = playerRef.current.videoHeight()
      var videoAspect = videoWidth / videoHeight

      if (isNaN(videoAspect)) {
        videoAspect = 16 / 9
        if (playerAspect < videoAspect) {
          videoWidth = playerWidth
          videoHeight = (playerWidth / 16) * 9
        } else {
          videoWidth = (playerHeight / 9) * 16
          videoHeight = playerHeight
        }
      }

      if (playerAspect < videoAspect) {
        var widthRatio = playerWidth / videoWidth
        var actualVideoHeight = widthRatio * videoHeight
        props.onResize(
          playerWidth,
          actualVideoHeight,
          0,
          (playerHeight - actualVideoHeight) / 2
        )
      } else {
        var heightRatio = playerHeight / videoHeight
        var actualVideoWidth = heightRatio * videoWidth
        props.onResize(
          actualVideoWidth,
          playerHeight,
          (playerWidth - actualVideoWidth) / 2,
          0
        )
      }
    }
  }

  // wrap the player in a div with a `data-vjs-player` attribute
  // so videojs won't create additional wrapper in the DOM
  // see https://github.com/videojs/video.js/pull/3856
  return (
    <div
      data-testid="videojsplayer"
      className="c-player"
      style={{ width: '100%', height: '100%' }}
    >
      <div
        className="c-player__screen vjs-fill"
        data-vjs-player="true"
        style={{ width: '100%', height: '100%' }}
      >
        <video
          ref={(node: HTMLVideoElement) => (videoNode = node)}
          className="video-js"
        />
      </div>
    </div>
  )
}

/**
 * Create an additional button on the control bar
 * See: https://stackoverflow.com/questions/35604358/videojs-v5-adding-custom-components-in-es6-am-i-doing-it-right
 */
export type ToggleSizeButtonOptions = {
  onPress: () => void
  icon: string
  text: string
}
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
 * Takes a timestamp in seconds and converts it to a string
 * with the format mm:ss:ms
 * @param {number} time The time in seconds
 * @returns {string} The time formatted as mm:ss
 */
export function PrintTimestamp(time: number): string {
  let min = Math.floor(time / 60)
  //toFixed(1) makes it so it is rounded to 1 decimal
  let sec = (time % 60).toFixed(1)
  //to make it look pretty
  if (parseFloat(sec) < 10) sec = '0' + sec
  return min + ':' + sec
}

/**
 * Takes the filename of a segment of the stream and
 * determines the time of the video when this segment started
 * @param {string} segName The filename of the segment
 * @returns {number} The time in seconds
 */
export function GetSegmentStarttime(segName: string): number {
  //Assuming the forwarder will always send a stream using
  //HLS, which gives .ts files afaik
  if (!segName.endsWith('.ts')) {
    console.warn(
      'GetSegmentStarttime: expected .ts file but got something else'
    )
    return NaN
  }

  //filename should contain '_V' if it comes from the forwarder
  if (segName.indexOf('_V') === -1) {
    console.warn('Video file not from forwarder')
    return NaN
  }

  //filename ends with _VXYYY.ts where X is a version
  //and YYY is the segment number
  let end = segName.split('_V')[1]
  let number = end.slice(1, end.length - 3) //remove the X and the .ts
  //The segments have a certain length, so multiply the number with the length for the time
  //TODO: make this not hardcoded
  return (parseInt(number) - 1) * 2
}
