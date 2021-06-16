/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React, { useState, useRef, useContext } from 'react'
import { Queue } from 'queue-typescript'
import { Modal, notification, Typography } from 'antd'

import { indicator } from '../pages/home'
import { VideoPlayer } from './videojsPlayer'
import { Box, QueueItem } from '../classes/clientMessage'
import { websocketContext } from './websocketContext'
import {
  StartOrchestratorMessage,
  StopOrchestratorMessage
} from '../classes/orchestratorMessage'
import { stream, source } from '../classes/source'
import { size } from '../classes/size'
import { colours } from '../utilities/colours'

/** Props for the overlay component, containing info on what camera feed the overlay belongs to and wether to draw boxes. */
export type overlayProps = {
  source: stream
  showBoxes: indicator
  hiddenObjectTypes: string[]
  autoplay: boolean
  onPrimary: () => void
  sources: source[]
}

/**
 * Component that takes a videoplayer component, and creates an overlay on top of it
 * to draw the bounding boxes received from the orchestrator.
 * @param props Properties for the overlay.
 * @returns An overlay containing a videojs player and a component that receives and draws bounding boxes over it.
 */
export function Overlay(props: overlayProps) {
  // Queue which keeps the incoming bounding boxes and the frameID at which they should be drawn.
  const queueRef = useRef(new Queue<QueueItem>())

  // The frameID the video player is currently displaying.
  const playerFrameIdRef = useRef(0)

  // If the video player is paused or not.
  const playerPlayingRef = useRef(props.autoplay)

  // The actual player, to get the image from.
  const snapRef = useRef<(box: Box) => string | undefined>(() => undefined)

  // A ref to the overlay itself, to scroll to.
  const thisRef = useRef<HTMLDivElement>(null)

  // A list to keep track of recently seen object ids.
  const seenRef = useRef<number[]>([])

  // State containing the boxes to be drawn this frame.
  const [item, setItem] = useState<QueueItem>()

  // State containing videoplayer dimensions/position on the page.
  const [size, setSize] = useState<size>({
    // Initial value.
    width: 10,
    height: 10,
    left: 10,
    top: 10
  })

  // State to keep track of the outline and a removeal timeout.
  const [outline, setOutline] = useState<{
    visible: boolean
    timeout?: NodeJS.Timeout
  }>({
    visible: false
  })

  // Access the websocket in order to create a listener for receiving boundingbox updates.
  const socketContext = useContext(websocketContext)

  React.useEffect(() => {
    /* Create a listener for the websocket which receives boundingbox messages.
     * Put the messages in a Queue so the boxes are kept until it's time to draw them. */
    var id = socketContext.addListener(
      props.source.id,
      (boxes: Box[], fID: number) => {
        /* Only accept new bounding boxes when the video is actually playing.
         * This prevents the boxes from updating while the video is paused. */
        if (playerPlayingRef.current) {
          queueRef.current.enqueue(new QueueItem(fID, boxes))
        }
      }
    )
    // Start an interval to take boxes from the queue for drawing.
    setInterval(() => handleQueue(), 1000 / 24)
    return () => socketContext.removeListener(id)
  }, [])

  /**
   * Dequeues boundingboxes until a set of boxes is found that correspond to the current frameID.
   * Once the correct set of boxes has been reached it will set these to be drawn.
   */
  function handleQueue() {
    // Keep dequeueing until a set of boxes with matching frameID is reached.
    while (playerFrameIdRef.current >= queueRef.current.front?.frameId) {
      let item = queueRef.current.dequeue()
      let boxes: Box[] = item.boxes
      let objectIds: number[] = []

      // Create a notification for every new objectid.
      boxes.forEach((box) => {
        if (box.objectId) {
          // Save the object, so it's not seen again.
          objectIds.push(box.objectId)
          if (!seenRef.current.includes(box.objectId)) Reappear(box.objectId)
        }
      })

      // Replace the seen objects.
      seenRef.current = objectIds

      setItem(item)
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
          setSnapCallback={(snap) => (snapRef.current = snap)}
          onTimestamp={(t) => (playerFrameIdRef.current = t)}
          onPlayPause={(p) => {
            playerPlayingRef.current = p
          }}
          onResize={setSize}
          autoplay={props.autoplay}
          controls={true}
          onPrimary={props.onPrimary}
          controlBar={{ pictureInPictureToggle: false }}
          sources={props.sources}
        />
      </div>
    </div>
  )

  /**
   * Function called when clicking on a bounding box when the object id is not set.
   * @param boxId The ID of the box that was clicked on.
   * @param frameId The frameID, or timestamp, when the box was clicked.
   */
  function onTrackingStart(box: Box, frameId: number) {
    // Get the box coordinates and take a snap.
    var snap = snapRef.current(box)

    Modal.confirm({
      title: 'Start tracking this object?',
      okButtonProps: { title: 'startTrackButton' },
      content: <img src={snap} style={{ outlineStyle: 'solid' }} />,
      width: 'auto',
      centered: true,
      onOk() {
        console.log('Start tracking', {
          cam: props.source,
          frame: frameId,
          box: box.boxId
        })

        socketContext.send(
          new StartOrchestratorMessage(
            props.source.id,
            frameId,
            box.boxId,
            snap
          )
        )
      },
      onCancel() {}
    })
  }

  /**
   * Function called when clicking on a bounding box when the object id is set.
   * @param objectId The ID of the object that is being tracked and will be untracked.
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

  /** Draws the overlay with the bounding boxes according to the setting of which boxes to display. */
  function DrawOverlay(): JSX.Element {
    if (!item) return <div />
    switch (props.showBoxes) {
      case 'All': {
        return DrawBoxes(item)
      }
      case 'Selection': {
        return DrawBoxes(
          new QueueItem(
            item.frameId,
            item.boxes.filter((x) => x.objectId !== undefined)
          )
        )
      }
      default: {
        return <div />
      }
    }
  }

  /**
   * Goes through all boxes given and draws then in the correct place on the overlay.
   * @param boxes The list of bounding boxes to draw.
   * @param frameId The timestamp when these boxes are being drawn.
   */
  function DrawBoxes(item: QueueItem): JSX.Element {
    return (
      <div>
        {item.boxes
          .filter(
            (box) =>
              !props.hiddenObjectTypes.some(
                (hiddenObjectType) => hiddenObjectType === box.objectType
              )
          )
          .map((box: Box) => {
            var { width, height, left, top } = box.toSize(
              size.width,
              size.height
            )
            var color = box.objectId ? colours[box.objectId % 102] : 'green'
            return (
              <div
                key={box.boxId}
                data-testid={`box-${box.boxId}`}
                style={{
                  position: 'absolute',
                  left: `${left + size.left}px`,
                  top: `${top + size.top}px`,
                  width: `${width}px`,
                  height: `${height}px`,
                  borderColor: color,
                  borderStyle: box.objectId ? 'solid' : 'dashed',
                  borderWidth: '2px',
                  transitionProperty: 'all',
                  transitionDuration: '100ms',
                  transitionTimingFunction: 'linear',
                  zIndex: 1000,
                  cursor: box.objectId === undefined ? 'pointer' : 'default'
                }}
                onClick={() => {
                  if (box.objectId === undefined)
                    onTrackingStart(box, item.frameId)
                  else onTrackingStop(box.objectId)
                }}
              >
                {
                  // Add an object id label above the bounding box, using a relative position and the border color.
                  box.objectId && (
                    <Typography.Text
                      style={{
                        position: 'relative',
                        top: '-25px',
                        left: '-2px',
                        border: color,
                        borderStyle: 'solid',
                        borderWidth: '2px',
                        backgroundColor: 'white',
                        color: 'black'
                      }}
                    >
                      {box.objectId}
                    </Typography.Text>
                  )
                }
              </div>
            )
          })}
      </div>
    )
  }

  /**
   * Open a notification which can be clicked on to go to a reappeared object.
   * @param objectId The object that reappeared.
   */
  function Reappear(objectId: number) {
    // Close other messages of this object, as they are no longer needed.
    notification.close(objectId.toString())
    notification.open({
      key: objectId.toString(),
      message: 'Subject reappeared',
      description: `object ${objectId} was found on camera ${props.source.name}`,
      onClick: () => {
        // Close the message, as it is not needed anymore.
        notification.close(objectId.toString())

        // Cancel the existing timeout so it does not remove the outline prematurely.
        if (outline.timeout) clearTimeout(outline.timeout)

        // Start a timeout to remove the badge.
        var timeout = setTimeout(() => {
          setOutline({ visible: false, timeout: undefined })
        }, 2000)

        // Set the badge, with the new timeout.
        setOutline({ visible: true, timeout: timeout })

        // Scroll to the video, so the user can see it.
        thisRef.current?.scrollIntoView({ behavior: 'smooth' })
      },
      placement: 'bottomRight',
      bottom: 5
    })
  }
}
