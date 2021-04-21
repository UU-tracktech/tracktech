/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React, { Fragment } from 'react'
import { Queue } from 'queue-typescript'

import { indicator } from '../pages/home'
import { VideoPlayer, VideoPlayerProps } from './videojsPlayer'
import { Box } from '../classes/clientMessage'
import { websocketContext } from './websocketContext'
import { StartOrchestratorMessage } from '../classes/orchestratorMessage'

export type overlayProps = { cameraId: string, showBoxes: indicator }
type overlayState = { boxes: Box[], frameId: number, width: number, height: number, left: number, top: number }
export class Overlay extends React.Component<overlayProps & VideoPlayerProps, overlayState> {

  queue = new Queue<Box[]>()

  static contextType = websocketContext
  context!: React.ContextType<typeof websocketContext>

  constructor(props: any) {
    super(props)
    this.state = { boxes: [], frameId: 0, width: 100, height: 100, left: 100, top: 100 }
  }

  onPlayerResize(width: number, height: number, left: number, top: number) {
    this.setState({ width: width, height: height, left: left, top: top })
  }

  componentDidMount() {
    this.context.addListener(this.props.cameraId, (boxes: Box[], frameId: number) => {
      this.setState({ boxes: boxes, frameId: frameId })
    })
  }

  /*  enqueue(message: ClientMessage) {
       this.queue.enqueue(message)
       this.setState({ queueLength: this.queue.length })
   }
 
   dequeue(): ClientMessage {
       var message = this.queue.dequeue()
       this.setState({ queueLength: this.queue.length })
       return message
   }
   
   
  clearQueue() {
      this.queue = new Queue<ClientMessage>()
      this.setState({ queueLength: this.queue.length })
  }*/

  render() {
    const colordict = { 0: 'red', 1: 'green', 2: 'blue' }

    return <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      <div style={{ position: 'absolute', width: '100%', height: '100%', overflow: 'hidden' }}>
        { this.DrawOverlay() }
      </div>
      <div style={{ position: 'absolute', width: '100%', height: '100%' }}>
        <VideoPlayer onResize={(w, h, l, t) => this.onPlayerResize(w, h, l, t)} autoplay={false} controls={true} onButtonClick={() => this.props.onButtonClick()} sources={this.props.sources} />
      </div>
    </div >
  }

  onBoxClick(boxId: number, frameId: number){
    if(window.confirm("Start tracking this object?")){
      this.context.send(new StartOrchestratorMessage(this.props.cameraId, frameId, boxId))
    }
  }

  DrawOverlay(): JSX.Element {
    switch (this.props.showBoxes) {
      case "All": {
        return this.DrawBoxes(this.state.boxes, this.state.frameId);
      }
      case "Selection": {
        return this.DrawBoxes(this.state.boxes.filter(x => x.objectId != undefined), this.state.frameId);
      }
      default : {
        return <div/>
      }
    }
  }

  DrawBoxes(boxes: Box[], frameId: number): JSX.Element{
    // TODO: make sure objectIds can be infinitely big without causing an index out of bounds
    var colordict : string[] = ["Green", "Red", "Yellow", "Blue", "Purple", "Brown", "Aqua", "Navy"] 

    return <Fragment>
          {
            boxes.map((box) => {
              var x1 = box.rect[0], x2 = box.rect[2], y1 = box.rect[1], y2 = box.rect[3]
              if (x1 > x2) {
                var tempx = x1
                x1 = x2
                x2 = tempx
              }
              if (y1 > y2) {
                var tempy = y1
                y1 = y2
                y2 = tempy
              }

              return <div key={box.boxId} style={
                {
                  position: 'absolute',
                  left: `${x1 * this.state.width + this.state.left}px`, top: `${y1 * this.state.height + this.state.top}px`,
                  width: `${(x2 - x1) * this.state.width}px`, height: `${(y2 - y1) * this.state.height}px`,
                  borderColor: colordict[box.objectId ?? 0], borderStyle: 'solid',
                  /* transitionProperty: 'all', transitionDuration: '1s', */
                  zIndex: 1000,
                  cursor: box.objectId === undefined ? "pointer" : "default"
                }
              } onClick={() => {if(box.objectId === undefined) this.onBoxClick(box.boxId, this.state.frameId)}} />
            })
          }
        </Fragment>
  }
}