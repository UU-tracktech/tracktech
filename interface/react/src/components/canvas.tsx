import React from "react"
import { Queue } from 'queue-typescript'

import { Box } from '../classes/ClientMessage'
import { websocketContext } from '../components/websocketContext'

export type canvasProps = { cameraId: number, width: number, height: number }
export class Canvas extends React.Component<canvasProps> {

    canvas = React.createRef<HTMLCanvasElement>()
    queue = new Queue<Box>()

    static contextType = websocketContext
    context!: React.ContextType<typeof websocketContext>

    componentDidMount() {
        this.context.addListener(this.props.cameraId, (boxes: Box[]) => this.drawBoxes(boxes))
    }

    drawBoxes(boxes: Box[]) {
        var canvas = this.canvas.current
        if (canvas) {
            var ctx = canvas.getContext('2d')
            if (ctx) {
                this.clear(ctx)

                boxes.forEach(box => {
                    if (ctx) this.drawBox(ctx, box)
                })
            }
        }
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

    clear(ctx: CanvasRenderingContext2D) {
        ctx.clearRect(0, 0, this.props.width, this.props.height)
    }

    drawBox(ctx: CanvasRenderingContext2D, box: Box) {
        var canvas = this.canvas.current

        if (canvas) {
            var rect = canvas.getBoundingClientRect()
            var x1 = rect.width * box.x1
            var y1 = rect.width * box.y1
            var x2 = rect.width * box.x2
            var y2 = rect.width * box.y2

            this.clear(ctx)
            this.drawRectangle(ctx, x1, y1, x2, y2)
        }
    }

    drawRectangle(ctx: CanvasRenderingContext2D, x1: number, y1: number, x2: number, y2: number, type: number = 0) {
        const colordict = { 0: 'red', 1: 'green', 2: 'blue' }

        ctx.strokeStyle = colordict[type]
        ctx.strokeRect(x1, y1, x2 - x1, y2 - y1)
    }

    handleMouseDown(event: React.MouseEvent<HTMLCanvasElement, MouseEvent>) {
        var canvas = this.canvas.current

        if (canvas) {
            var rect = canvas.getBoundingClientRect()
            var x = event.clientX - rect.left
            var y = event.clientY - rect.top

            var ctx = canvas.getContext('2d')
            if (ctx) {
                this.clear(ctx)
                this.drawRectangle(ctx, x - 10, y - 10, x + 10, y + 10, 1)
            }
        }
    }

    render() {
        return <div>
            < canvas
                key={this.props.cameraId}
                style={{ position: 'absolute', zIndex: 1000 }}
                width={this.props.width}
                height={this.props.height}
                ref={this.canvas}
                onClick={(event) => this.handleMouseDown(event)}
            />
            <div>
                {this.props.children}
            </div>
        </div >
    }
}