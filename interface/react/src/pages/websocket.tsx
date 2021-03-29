import { Component } from 'react'
import { Button, Form } from 'react-bootstrap'
import { Queue } from 'queue-typescript'

import { OrchestratorMessage, StartOrchestratorMessage, StopOrchestratorMessage, TestOrchestratorMessage } from '../classes/OrchestratorMessage'
import { ClientMessage, BoxesClientMessage } from '../classes/ClientMessage'

type Message = { dateTime: Date, content: ClientMessage }
type connectionState = 'NONE' | 'CONNECTING' | 'OPEN' | 'CLOSING' | 'CLOSED' | 'ERROR'
type WebsocketUserState = { socketUrl: string, connectionState: connectionState, queueLength: number, currentMessage?: Message }
export class WebsocketUser extends Component<{}, WebsocketUserState> {

  socket?: WebSocket
  queue = new Queue<Message>()

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

  enqueue(message: Message) {
    this.queue.enqueue(message)
    this.setState({ queueLength: this.queue.length })
  }

  dequeue(): Message {
    var message = this.queue.dequeue()
    this.setState({ queueLength: this.queue.length })
    return message
  }

  clearQueue() {
    this.queue = new Queue<Message>()
    this.setState({ queueLength: this.queue.length })
  }

  onOpen(ev: Event) {
    console.log('connected socket')
    this.setState({ connectionState: 'OPEN' })
  }

  onMessage(ev: MessageEvent<any>) {
    console.log('socket message', ev.data)
    var content: ClientMessage = JSON.parse(ev.data)
    var message: Message = { dateTime: new Date(), content: content }
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
      <div>
        <p>URL: {this.state.socketUrl}</p>
        <p>STATE: {this.state.connectionState}</p>
        <p>QUEUE LENGTH: {this.state.queueLength}</p>

        <Form>
          <Button onClick={() => this.setSocket('wss://tracktech.ml:50010/client')}>Change Socket Url</Button>
          <Button disabled={this.state.connectionState !== 'OPEN'} onClick={() => this.send(new TestOrchestratorMessage(1))}>Send test json</Button>
          <Button disabled={this.state.connectionState !== 'OPEN'} onClick={() => this.send(new StartOrchestratorMessage(1, 2, 3))}>Send start json</Button>
          <Button disabled={this.state.connectionState !== 'OPEN'} onClick={() => this.send(new StopOrchestratorMessage(1))}>Send stop json</Button>
        </Form>

        <Form>
          <Button onClick={() => this.setState({ currentMessage: this.dequeue() })}>Dequeue</Button>
          <Button onClick={() => this.clearQueue()}>Clear queue</Button>
        </Form>

        {
          this.state.currentMessage && <div>
            <p>AT: {this.state.currentMessage.dateTime.toUTCString()}</p>
            <p>CONTENT: {JSON.stringify(this.state.currentMessage.content)}</p>
          </div>
        }

      </div>
    )
  }
}