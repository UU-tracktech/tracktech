import React, {Component} from "react";

export default class Canvas1 extends React.Component{

    //canvasRef = () => { return useRef(null)}

    componentDidMount = () => {
        const canvas = document.getElementById('canvas') as HTMLCanvasElement;
        const ctx = canvas.getContext('2d');

        ctx!.fillStyle = "green";

        requestAnimationFrame(this.tick);
    }

    tick = () => {
        if(this.state.showBoxes){
            const canvas = document.getElementById('canvas') as HTMLCanvasElement;
            const ctx = canvas.getContext('2d');
            ctx!.clearRect(0, 0, 300, 300);
            this.state.x1 += 1;
            this.state.x2 += 1;
            this.state.y1 += 1;
            this.state.y2 += 1;
            ctx!.strokeRect(this.state.x1, this.state.y1, this.state.x2, this.state.y2);
            requestAnimationFrame(this.tick);
        }
        else{
            this.state.x1 = 10;
            this.state.y1 = 10;
            this.state.x2 = 150;
            this.state.y2 = 150;
        }


    }

    handleMouseDown = (event) => {
        const {x, y} = event;
        console.log(x, y);
        const canvas = document.getElementById('canvas') as HTMLCanvasElement;
        const ctx = canvas.getContext('2d');
        ctx!.clearRect(0, 0, 300, 300);

        //Displaying or undisplaying bounding boxes
        this.state.showBoxes = !this.state.showBoxes;

        if(this.state.showBoxes){
            ctx!.strokeRect(10, 10, 150, 150);
            requestAnimationFrame(this.tick);
        }

    }

    state = {
        showBoxes: false,
        x1: 10,
        y1: 10,
        x2: 150,
        y2: 150
    }

    render(){
        return <canvas
            id='canvas'
            style={{backgroundColor: 'blue'}}
            height='300'
            width='300'
            onMouseDown = {this.handleMouseDown}
        >Canvas</canvas>
    }
}


