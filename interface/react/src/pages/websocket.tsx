import React, { Component } from 'react'
import WebSocket from "../components/WebSocket"
import '../components/WebSocket.css'

export class Websocket extends Component {

  render() {
    return (
      <div>
        <WebSocket />
      </div>
    )
  }
}