/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

/**
  This component takes a videoplayer component, and creates an overlay on top of it
  to draw the bounding boxes received from the orchestrator
*/

import React, { useState, useRef, useContext } from 'react'
import { Queue } from 'queue-typescript'
import { Modal, notification } from 'antd'

import { indicator } from '../pages/home'
import { VideoPlayer, VideoPlayerProps } from './videojsPlayer'
import { Box, QueueItem } from '../classes/clientMessage'
import { websocketContext } from './websocketContext'
import {
  StartOrchestratorMessage,
  StopOrchestratorMessage
} from '../classes/orchestratorMessage'
import { source } from '../classes/source'

// The overlayprops contain info on what camera feed the overlay belongs to and wheter to draw boxes or not
export type overlayProps = {
  source: source
  showBoxes: indicator
  hiddenObjectTypes: string[]
  autoplay: boolean
}

// The size of the overlay, used to scale the drawing of the bounding boxes
type size = { width: number; height: number; left: number; top: number }

export function Overlay(props: overlayProps & VideoPlayerProps) {
  // Queue which keeps the incoming bounding boxes and the frameID at which they should be drawn
  const queueRef = useRef(new Queue<QueueItem>())

  // The frameID the video player is currently displaying
  const playerFrameIdRef = useRef(0)

  // The frameID of the boxes that are currently drawn
  const frameIdRef = useRef(0)

  // If the video player is paused or not
  const playerPlayingRef = useRef(props.autoplay)

  // A ref to the overlay itself
  const thisRef = useRef<HTMLDivElement>(null)

  // A list to keep track of recently seen object ids
  const seenRef = useRef<number[]>([])

  // State containing the boxes to be drawn this frame
  const [boxes, setBoxes] = useState<Box[]>([])

  // State containing videoplayer dimensions/position on the page
  const [size, setSize] = useState<size>({
    //initial value
    width: 10,
    height: 10,
    left: 10,
    top: 10
  })

  //State to keep track of the outline and a removeal timeout
  const [outline, setOutline] = useState<{
    visible: boolean
    timeout?: NodeJS.Timeout
  }>({
    visible: false
  })

  //Access the websocket in order to create a listener for receiving boundingbox updates
  const socketContext = useContext(websocketContext)

  React.useEffect(() => {
    //Create a listener for the websocket which receives boundingbox messages
    //Put the messages in a Queue so the boxes are kept until it's time to draw them
    var id = socketContext.addListener(
      props.source.id,
      (boxes: Box[], fID: number) => {
        //only accept new bounding boxes when the video is actually playing
        //This prevents the boxes from updating while the video is paused
        if (playerPlayingRef.current) {
          queueRef.current.enqueue(new QueueItem(fID, boxes))
        }
      }
    )
    //Start an interval to take boxes from the queue for drawing
    setInterval(() => handleQueue(), 1000 / 24)
    return socketContext.removeListener(id)
  }, [])

  /**
   * Dequeues boundingboxes until a set of boxes is found that correspond to the current frameID
   * Once the correct set of boxes has been reached it will set these to be drawn
   */
  function handleQueue() {
    //Keep dequeueing until a set of boxes with matching frameID is reached
    while (playerFrameIdRef.current >= frameIdRef.current) {
      if (queueRef.current.length == 0) break
      var boxes: Box[] = queueRef.current.dequeue().boxes
      var objectIds: number[] = []

      //Create a notification for every new objectid
      boxes.forEach((box) => {
        if (box.objectId) {
          //Save the object, so we do not see it again
          objectIds.push(box.objectId)
          if (!seenRef.current.includes(box.objectId)) Reappear(box.objectId)
        }
      })

      //Replace the seen objects
      seenRef.current = objectIds

      setBoxes(boxes)
    }
  }

  return (
    <div
      data-testid={'overlayDiv'}
      style={{
        position: 'relative',
        width: '100%',
        height: '100%',
        outline: '#096dd9',
        outlineStyle: outline.visible ? 'solid' : 'none'
      }}
      ref={thisRef}
    >
      <div
        style={{
          position: 'absolute',
          width: '100%',
          height: '100%',
          overflow: 'hidden'
        }}
      >
        {DrawOverlay()}
      </div>
      <div style={{ position: 'absolute', width: '100%', height: '100%' }}>
        <VideoPlayer
          onTimestamp={(t) => (playerFrameIdRef.current = t)}
          onPlayPause={(p) => {
            playerPlayingRef.current = p
          }}
          onResize={(w, h, l, t) =>
            setSize({ width: w, height: h, left: l, top: t })
          }
          autoplay={props.autoplay}
          controls={true}
          onPrimary={props.onPrimary}
          sources={props.sources}
        />
      </div>
    </div>
  )

  /**
   * Function called when clicking on a bounding box when the object id is not set
   * @param boxId The ID of the box that was clicked on
   * @param frameId The frameID, or timestamp, when the box was clicked
   */
  function onTrackingStart(boxId: number, frameId: number) {
    Modal.confirm({
      title: 'Start tracking this object?',
      okButtonProps: { title: 'startTrackButton' },
      onOk() {
        console.log('Start tracking', {
          cam: props.source,
          frame: frameId,
          box: boxId
        })

        socketContext.send(
          new StartOrchestratorMessage(props.source.id, frameId, boxId)
        )
      },
      onCancel() {}
    })
  }

  /**
   * Function called when clicking on a bounding box when the object id is set
   * @param objectId The ID of the object that is being tracked and will be untracked
   */
  function onTrackingStop(objectId: number) {
    Modal.confirm({
      title: 'Stop tracking this object?',
      onOk() {
        console.log('Stop tracking ', objectId)
        socketContext.send(new StopOrchestratorMessage(objectId))
      },
      onCancel() {}
    })
  }

  /**
   * Draws the overlay with the bounding boxes according to the setting of which boxes to display
   */
  function DrawOverlay(): JSX.Element {
    switch (props.showBoxes) {
      case 'All': {
        return DrawBoxes(boxes, frameIdRef.current)
      }
      case 'Selection': {
        return DrawBoxes(
          boxes.filter((x) => x.objectId !== undefined),
          frameIdRef.current
        )
      }
      default: {
        return <div />
      }
    }
  }

  /**
   * Goes through all boxes given and draws then in the correct place on the overlay
   * @param boxes The list of bounding boxes to draw
   * @param frameId The timestamp when these boxes are being drawn
   */
  function DrawBoxes(boxes: Box[], frameId: number): JSX.Element {
    // TODO: make sure objectIds can be infinitely big without causing an index out of bounds
    var colordict: string[] = [
      'Green',
      'Red',
      'Yellow',
      'Blue',
      'Purple',
      'Brown',
      'Aqua',
      'Navy'
    ]

    return (
      <div>
        {boxes
          .filter(
            (box) =>
              /* eslint-disable react/prop-types */
              !props.hiddenObjectTypes.some(
                (hiddenObjectType) => hiddenObjectType === box.objectType
              )
          )
          .map((box) => {
            var x1 = box.rect[0],
              x2 = box.rect[2],
              y1 = box.rect[1],
              y2 = box.rect[3]
            if (x1 > x2) [x1, x2] = [x2, x1]
            if (y1 > y2) [y1, y2] = [y2, y1]

            return (
              <div
                key={box.boxId}
                data-testid={`box-${box.boxId}`}
                style={{
                  position: 'absolute',
                  left: `${x1 * size.width + size.left}px`,
                  top: `${y1 * size.height + size.top}px`,
                  width: `${(x2 - x1) * size.width}px`,
                  height: `${(y2 - y1) * size.height}px`,
                  borderColor: colordict[box.objectId ?? 0],
                  borderStyle: 'solid',
                  transitionProperty: 'all',
                  transitionDuration: '100ms',
                  transitionTimingFunction: 'linear',
                  zIndex: 1000,
                  cursor: box.objectId === undefined ? 'pointer' : 'default'
                }}
                onClick={() => {
                  if (box.objectId === undefined)
                    onTrackingStart(box.boxId, frameId)
                  else onTrackingStop(box.objectId)
                }}
              />
            )
          })}
      </div>
    )
  }

  /**
   * Open a notification which can be clicked on to go to a reappeared object
   * @param objectId The object that reappeared
   */
  function Reappear(objectId: number) {
    //Close other messages of this object, as they are no longer needed
    notification.close(objectId.toString())
    notification.open({
      key: objectId.toString(),
      message: 'Subject reappeared',
      description: `object ${objectId} was found on camera ${props.source.name}`,
      onClick: () => {
        //Close the message, as it is not needed anymore
        notification.close(objectId.toString())

        //Cancel the existing timeout so it does not remove the outline prematurely
        if (outline.timeout) clearTimeout(outline.timeout)

        //Start a timeout to remove the badge
        var timeout = setTimeout(() => {
          setOutline({ visible: false, timeout: undefined })
        }, 2000)

        //Set the badge, with the new timeout
        setOutline({ visible: true, timeout: timeout })

        //Scroll to the video, so we can see it
        thisRef.current?.scrollIntoView({ behavior: 'smooth' })
      },
      placement: 'bottomRight',
      bottom: 5
    })
  }
}
