/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import videojs from 'video.js'
import 'video.js/dist/video-js.css'
import 'bootstrap-icons/font/bootstrap-icons.css'

export type VideoPlayerProps = { onUp: () => void, onDown: () => void, onResize?: (width: number, height: number, left: number, top: number) => void } & videojs.PlayerOptions
export function VideoPlayer(props: VideoPlayerProps) {
  var videoNode: HTMLVideoElement

  const playerRef = React.useRef<videojs.Player>()

  const initialUriIntervalRef = React.useRef<number>()
  const changeIntervalRef = React.useRef<number>()
  const updateIntervalRef = React.useRef<number>()

  var startUri    //The first URI the player gets
  var startTime   //The timestamp where the player started
  var timeStamp

  React.useEffect(() => {
    // instantiate video.js
    playerRef.current = videojs(videoNode, props, () => {
      var player = playerRef.current

      player?.controlBar.addChild(new resizeButton(player, { onPress: props.onUp, icon: 'bi-zoom-in', text: 'Increase size' }), {}, 0)
      player?.controlBar.addChild(new resizeButton(player, { onPress: props.onDown, icon: 'bi-zoom-out', text: 'Decrease size' }), {}, 1)
      player?.on('playerresize', () => onResize())
      player?.on('play', () => onResize())

      //Timestamp stuff

      /* On the first time a stream is started, attempt getting the
         URI and keep going with the interval until one is obtained */
      player?.on('firstplay', () => {
        initialUriIntervalRef.current = player?.setInterval(() => {
          getInitialUri()
        }, 200)
      })

      player?.on('play', () => {
        updateIntervalRef.current = player?.setInterval(() => {
          updateTimestamp()
        }, 100)
      })

      /* Every time the stream is paused we can stop updating the
      * interval, player?.currentTime() will keep going in the
      * background anyway */
      player?.on('pause', () => {
        if (updateIntervalRef.current) player?.clearInterval(updateIntervalRef.current)
      })
    })

    return (() => playerRef.current?.dispose())
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  /**
   * Accesses the video player tech and returns the URI
   * from the first segment in the playlist
   */
  function getURI(): string | undefined {
    try {
      //passing any argument suppresses a warning about
      //accessing the tech
      let tech = playerRef.current?.tech({ randomArg: true })
      if (tech) {
        //ensure media is loaded before trying to access
        let med = tech['vhs'].playlists.media()
        if (med)
          return med.segments[0].uri
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
    let currentUri = getURI()
    if (currentUri) {
      console.log('InitialURI: ', currentUri)

      startUri = currentUri
      if (initialUriIntervalRef.current) playerRef.current?.clearInterval(initialUriIntervalRef.current)
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
        console.log('URI changed: ', currentUri)
        startTime = GetSegmentStarttime(currentUri)
        console.log('Starttime: ', PrintTimestamp(startTime))
        if (changeIntervalRef.current) playerRef.current?.clearInterval(changeIntervalRef.current)
      }
    }
  }

  /**
   * Should be done in an interval, started whenever the user hits play
   * this interval should be stopped whenever the user pauses
   */
  function updateTimestamp() {

    if (!startTime) {
      console.log('Timestamp: Loading...')
      return
    }

    let currentPlayer = playerRef.current?.currentTime()
    //dont ask why -4, it just works
    timeStamp = startTime + currentPlayer - 4

    //print this videoplayer info to console as 1 object
    let toPrint = {
      timeStamp: PrintTimestamp(timeStamp),
      frameID: timeStamp,            //ID in seconds
      //frameID: this.timeStamp / 1000,   //ID in ms
    }
    console.log(toPrint)
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
        props.onResize(playerWidth, playerHeight, 0, 0)
      }
      else if (playerAspect < videoAspect) {
        var widthRatio = playerWidth / videoWidth
        var actualVideoHeight = widthRatio * videoHeight
        props.onResize(playerWidth, actualVideoHeight, 0, (playerHeight - actualVideoHeight) / 2)
      } else {
        var heightRatio = playerHeight / videoHeight
        var actualVideoWidth = heightRatio * videoWidth
        props.onResize(actualVideoWidth, playerHeight, (playerWidth - actualVideoWidth) / 2, 0)
      }
    }
  }

  // wrap the player in a div with a `data-vjs-player` attribute
  // so videojs won't create additional wrapper in the DOM
  // see https://github.com/videojs/video.js/pull/3856
  return (
    <div className='c-player' style={{ width: '100%', height: '100%' }}>
      <div className='c-player__screen vjs-fill' data-vjs-player='true' style={{ width: '100%', height: '100%' }}>
        <video ref={(node: HTMLVideoElement) => videoNode = node} className='video-js' />
      </div>
    </div>
  )
}

/**
 * Create an additional button on the control bar
 * See: https://stackoverflow.com/questions/35604358/videojs-v5-adding-custom-components-in-es6-am-i-doing-it-right
 */
export type ToggleSizeButtonOptions = { onPress: () => void, icon: string, text: string }
class resizeButton extends videojs.getComponent('Button') {

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
 * @returns {string} The time formatted as mm:ss:ms
 */
function PrintTimestamp(time: number): string {

  let min = Math.floor(time / 60)
  //toFixed(1) makes it so it is rounded to 1 decimal
  let sec = (time % 60).toFixed(1)
  //to make it look pretty
  if (parseFloat(sec) < 10)
    sec = '0' + sec
  return min + ':' + sec
}

/**
 * Takes the filename of a segment of the stream and
 * determines the time of the video when this segment started
 * @param {string} segName The filename of the segment
 * @returns {number} The time in seconds
 */
function GetSegmentStarttime(segName: string): number {

  //Assuming the forwarder will always send a stream using
  //HLS, which gives .ts files afaik
  if (!segName.endsWith('.ts')) {
    console.warn('GetSegmentStarttime: ' +
      'expected .ts file but got something else')
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
  let number = end.slice(1, end.length - 3)
  //Every segment is 2 seconds, therefore
  //the number * 2 is the timestamp
  return parseInt(number) * 2
}