import React, { Component } from 'react'
import { Queue } from 'queue-typescript'

import { OrchestratorMessage, StartOrchestratorMessage, StopOrchestratorMessage, TestOrchestratorMessage } from '../classes/OrchestratorMessage'
import { ClientMessage, BoxesClientMessage } from '../classes/ClientMessage'

export type connectionState = 'NONE' | 'CONNECTING' | 'OPEN' | 'CLOSING' | 'CLOSED' | 'ERROR'

export type websocketArgs = {
  setSocket: (url: string) => void
  send: (message: OrchestratorMessage) => void
  dequeue: () => ClientMessage
  clearQueue: () => void
  queueLength: number
  connectionState: connectionState
  socketUrl: string
}

export const websocketContext = React.createContext<websocketArgs>({
  setSocket: (url: string) => alert(JSON.stringify(url)),
  send: (message: OrchestratorMessage) => alert(JSON.stringify(message)),
  dequeue: () => new BoxesClientMessage(0, 0, []),
  clearQueue: () => { },
  queueLength: 0,
  connectionState: 'NONE',
  socketUrl: 'NO URL'
})

type WebsocketProviderState = { socketUrl: string, connectionState: connectionState, queueLength: number }
export class WebsocketProvider extends Component<{}, WebsocketProviderState> {

  socket?: WebSocket
  queue = new Queue<ClientMessage>()

  constructor(props: any) {
    super(props)

    this.state = { connectionState: 'NONE', socketUrl: 'wss://echo.websocket.org', queueLength: 0 }
    this.setSocket(this.state.socketUrl)
  }
  setSocket(url: string) {
    this.socket = new WebSocket(url)
    this.setState({ connectionState: 'CONNECTING' })
    this.socket.onopen = (ev: Event) => this.onOpen(ev)
    this.socket.onmessage = (ev: MessageEvent<any>) => this.onMessage(ev)
    this.socket.onclose = (ev: CloseEvent) => this.onClose(ev)
    this.socket.onerror = (ev: Event) => this.onError(ev)
    this.setState({ socketUrl: url })
  }

  enqueue(message: ClientMessage) {
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
  }

  onOpen(ev: Event) {
    console.log('connected socket')
    this.setState({ connectionState: 'OPEN' })
  }

  onMessage(ev: MessageEvent<any>) {
    console.log('socket message', ev.data)
    var message: ClientMessage = JSON.parse(ev.data)
    this.enqueue(message)
  }

  onClose(ev: CloseEvent) {
    console.log('closed socket')
    this.setState({ connectionState: 'CLOSED' })
  }

  onError(ev: Event) {
    console.log('socket error')
    this.setState({ connectionState: 'ERROR' })
  }


  send(message: OrchestratorMessage) {
    if (!this.socket) throw new Error('socket is undefined')
    this.socket.send(JSON.stringify(message))
  }

  render() {
    return (
      <websocketContext.Provider value={
        {
          setSocket: (url) => this.setSocket(url),
          send: (message) => this.send(message),
          dequeue: () => this.dequeue(),
          clearQueue: () => this.clearQueue(),
          queueLength: this.state.queueLength,
          connectionState: this.state.connectionState,
          socketUrl: this.state.socketUrl
        }}>
        {this.props.children}
      </websocketContext.Provider>
    )
  }
}