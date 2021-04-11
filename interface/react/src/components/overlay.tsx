import React from 'react'
import { Queue } from 'queue-typescript'

import { VideoPlayer, VideoPlayerProps } from '../components/VideojsPlayer'
import { Box } from '../classes/ClientMessage'
import { websocketContext } from './websocketContext'

export type overlayProps = { cameraId: number, onBoxClick: (id?: number) => void }
type overlayState = { boxes: Box[], width: number, height: number, left: number, top: number }
export class Overlay extends React.Component<overlayProps & VideoPlayerProps, overlayState> {

    queue = new Queue<Box[]>()

    static contextType = websocketContext
    context!: React.ContextType<typeof websocketContext>

    constructor(props: any) {
        super(props)
        this.state = { boxes: [], width: 100, height: 100, left: 100, top: 100 }
    }

    onPlayerResize(width: number, height: number, left: number, top: number) {
        this.setState({ width: width, height: height, left: left, top: top })
    }

    componentDidMount() {
        var cameraId = this.props.cameraId
        cameraId = 1
        this.context.addListener(cameraId, (boxes: Box[]) => {
            this.setState({ boxes: boxes })
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
                {
                    this.state.boxes.map((box) => {
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
                                borderColor: "blue" /*colordict[box.boxId ?? 0]*/, borderStyle: 'solid',
                                /* transitionProperty: 'all', transitionDuration: '1s', */
                                zIndex: 1000
                            }
                        } onClick={() => this.props.onBoxClick(box.boxId)} />
                    })
                }
            </div>
            <div style={{ position: 'absolute', width: '100%', height: '100%' }}>
                <VideoPlayer onResize={(w, h, l, t) => this.onPlayerResize(w, h, l, t)} autoplay={false} controls={true} onButtonClick={() => this.props.onButtonClick()} sources={this.props.sources} />
            </div>
        </div >
    }
}