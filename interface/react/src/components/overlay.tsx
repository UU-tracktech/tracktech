import React from "react"
import { Queue } from 'queue-typescript'

import { Box } from '../classes/ClientMessage'
import { websocketContext } from './websocketContext'

export type overlayProps = { cameraId: number, width: number, height: number, onClickCallback: (id?: number) => void }
type overlayState = { boxes: Box[] }
export class Overlay extends React.Component<overlayProps, overlayState> {

    canvas = React.createRef<HTMLCanvasElement>()
    queue = new Queue<Box[]>()

    static contextType = websocketContext
    context!: React.ContextType<typeof websocketContext>

    constructor(props: any) {
        super(props)
        this.state = { boxes: [] }
    }

    componentDidMount() {
        this.context.addListener(this.props.cameraId, (boxes: Box[]) => {
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
        return <div>
            <div style={{ position: 'absolute', width: this.props.width, height: this.props.height, overflow: 'hidden' }}>
                {
                    this.state.boxes.map((box) => <div key={box.type} style={
                        {
                            position: 'relative',
                            left: box.x1 * this.props.width, top: box.y1 * this.props.height, width: (box.x2 - box.x1) * this.props.width, height: (box.y2 - box.y1) * this.props.height,
                            borderColor: colordict[box.type ?? 0], borderStyle: 'solid',
                            transitionProperty: 'all', transitionDuration:'1s',
                            zIndex: 1000
                        }
                    } onClick={() => this.props.onClickCallback(box.id)} />)
                }
            </div>
            <div>
                {this.props.children}
            </div>
        </div >
    }
}