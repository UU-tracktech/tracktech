import React, { Component } from "react"

export class Canvas extends React.Component {

    canvas = React.createRef<HTMLCanvasElement>()

    componentDidMount = () => {
        const ctx = this.canvas.current?.getContext('2d')
        //const queue = require('../')
        //const q = queue({ results: [] })
        //this.state.queue = q
        ctx!.fillStyle = "green"

        requestAnimationFrame(this.tick)
    }

    tick = () => {
        if (this.state.showBoxes) {
            const ctx = this.canvas.current?.getContext('2d')
            ctx!.clearRect(0, 0, 300, 300)
            this.state.x1 += 1
            this.state.x2 += 1
            this.state.y1 += 1
            this.state.y2 += 1
            ctx!.strokeRect(this.state.x1, this.state.y1, this.state.x2, this.state.y2)
            requestAnimationFrame(this.tick)
        }
        else {
            this.state.x1 = 10
            this.state.y1 = 10
            this.state.x2 = 150
            this.state.y2 = 150
        }


    }

    handleMouseDown = (event) => {
        const { x, y } = event
        console.log(x, y)
        //if(this.state.queue != null) {
        // @ts-ignore
        //this.state.queue.push("Hello")
        //}
        const ctx = this.canvas.current?.getContext('2d')
        ctx!.clearRect(0, 0, 300, 300)
        //if(this.state.queue != null) {
        // @ts-ignore
        //console.log(this.state.queue.size)
        //}
        //Displaying or undisplaying bounding boxes
        this.state.showBoxes = !this.state.showBoxes

        if (this.state.showBoxes) {
            ctx!.strokeRect(10, 10, 150, 150)
            requestAnimationFrame(this.tick)
        }

    }

    state = {
        //Making a queue and saving it in the state.
        queue: null,
        showBoxes: false,
        x1: 10,
        y1: 10,
        x2: 150,
        y2: 150
    }

    render() {
        return <canvas
            ref={this.canvas}
            style={{ backgroundColor: 'blue' }}
            height='300'
            width='300'
            onMouseDown={this.handleMouseDown}
        >Canvas</canvas>
    }
}


