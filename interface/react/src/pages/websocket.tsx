import { Component } from 'react'
import { Button, ListGroup } from 'react-bootstrap'
import { OrchestratorMessage, StartOrchestratorMessage, StopOrchestratorMessage, TestOrchestratorMessage } from '../classes/OrchestratorMessage'
import { ClientMessage, BoxesClientMessage } from '../classes/ClientMessage'

type Message = { dateTime: Date, content: ClientMessage }
type connectionState = 'NONE' | 'CONNECTING' | 'OPEN' | 'CLOSING' | 'CLOSED' | 'ERROR'
type WebsocketUserState = { socketUrl: string, connectionState: connectionState, history: Message[] }
export class WebsocketUser extends Component<{}, WebsocketUserState> {

  socket?: WebSocket

  constructor(props: any) {
    super(props)

    this.state = { connectionState: 'NONE', socketUrl: 'wss://echo.websocket.org', history: [] }
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
    var message: ClientMessage = JSON.parse(ev.data)
    this.setState(oldState => ({ history: [...oldState.history, { dateTime: new Date(), content: message }] }))
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
        <span>URL: {this.state.socketUrl}</span>
        <span>STATE: {this.state.connectionState}</span>

        <Button onClick={() => this.setSocket('wss://tracktech.ml:50010/client')}>Change Socket Url</Button>
        <Button onClick={() => this.send(new TestOrchestratorMessage(1))}>Send test json</Button>
        <Button onClick={() => this.send(new StartOrchestratorMessage(1, 2, 3))}>Send start json</Button>
        <Button onClick={() => this.send(new StopOrchestratorMessage(1))}>Send stop json</Button>

        <ListGroup>
          {this.state.history.map((message: Message) =>
            <ListGroup.Item id={message.dateTime.toString()}>
              <p>AT: {message.dateTime.toUTCString()}</p>
              <p>CONTENT: {JSON.stringify(message.content)}</p>
            </ListGroup.Item>)}
        </ListGroup>
      </div>
    )
  }
}