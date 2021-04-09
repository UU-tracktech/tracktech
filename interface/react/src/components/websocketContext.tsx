import React, { Component } from 'react'
import { Queue } from 'queue-typescript'

import { OrchestratorMessage } from '../classes/OrchestratorMessage'
import { ClientMessage, Box } from '../classes/ClientMessage'

export type connectionState = 'NONE' | 'CONNECTING' | 'OPEN' | 'CLOSING' | 'CLOSED' | 'ERROR'

export type websocketArgs = {
  setSocket: (url: string) => void
  send: (message: OrchestratorMessage) => void
  addListener: (id: number, callback: (boxes: Box[]) => void) => void
  connectionState: connectionState
  socketUrl: string
}

export const websocketContext = React.createContext<websocketArgs>({
  setSocket: (url: string) => alert(JSON.stringify(url)),
  send: (message: OrchestratorMessage) => alert(JSON.stringify(message)),
  addListener: (_: number, _2: (boxes: Box[]) => void) => { },
  connectionState: 'NONE',
  socketUrl: 'NO URL'
})

type WebsocketProviderState = { socketUrl: string, connectionState: connectionState }
export class WebsocketProvider extends Component<{}, WebsocketProviderState> {

  socket?: WebSocket
  listeners: { id: number, callback: (boxes: Box[]) => void }[] = []
  queue = new Queue<ClientMessage>()

  constructor(props: any) {
    super(props)

    this.state = { connectionState: 'NONE', socketUrl: 'wss://tracktech.ml:50010/client' }
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

  onOpen(ev: Event) {
    console.log('connected socket')
    this.setState({ connectionState: 'OPEN' })
  }

  onMessage(ev: MessageEvent<any>) {
    console.log('socket message', ev.data)
    var message: any = JSON.parse(ev.data)
    this.listeners.filter((listener) => listener.id === message.cameraId).forEach((listener) => listener.callback(message.boxes))
  }

  onClose(ev: CloseEvent) {
    console.log('closed socket')
    this.setState({ connectionState: 'CLOSED' })
  }

  onError(ev: Event) {
    console.log('socket error')
    this.setState({ connectionState: 'ERROR' })
  }

  addListener(id: number, callback: (boxes: Box[]) => void) {
    this.listeners.push({ id: id, callback: callback })
  }

  send(message: OrchestratorMessage) {
    if (!this.socket) throw new Error('socket is undefined')
    this.socket.send(JSON.stringify(message))
  }

  render() {
    return (
      <websocketContext.Provider value={
        {
          setSocket: (url: string) => this.setSocket(url),
          send: (message: OrchestratorMessage) => this.send(message),
          addListener: (id: number, callback: (boxes: Box[]) => void) => this.addListener(id, callback),
          connectionState: this.state.connectionState,
          socketUrl: this.state.socketUrl
        }}>
        {this.props.children}
      </websocketContext.Provider>
    )
  }
}