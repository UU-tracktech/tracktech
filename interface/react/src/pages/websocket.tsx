import { Component } from 'react'
import { Button, Form } from 'react-bootstrap'

import { OrchestratorMessage, StartOrchestratorMessage, StopOrchestratorMessage, TestOrchestratorMessage } from '../classes/OrchestratorMessage'
import { ClientMessage, BoxesClientMessage } from '../classes/ClientMessage'
import { connectionState, websocketArgs, websocketContext } from '../components/websocketContext'

type WebsocketUserState = { currentMessage?: ClientMessage }
export class WebsocketUser extends Component<{}, WebsocketUserState> {

  constructor(props: any) {
    super(props)
    this.state = {}
  }

  render() {
    return (
      <websocketContext.Consumer>
        {
          ({ send, setSocket, dequeue, clearQueue, socketUrl, connectionState, queueLength }: websocketArgs) => <div>
            <p>URL: {socketUrl}</p>
            <p>STATE: {connectionState}</p>
            <p>QUEUE LENGTH: {queueLength}</p>

            <Form>
              <Button onClick={() => setSocket('wss://tracktech.ml:50010/client')}>Change Socket Url</Button>
              <Button disabled={connectionState !== 'OPEN'} onClick={() => send(new TestOrchestratorMessage(1))}>Send test json</Button>
              <Button disabled={connectionState !== 'OPEN'} onClick={() => send(new StartOrchestratorMessage(1, 2, 3))}>Send start json</Button>
              <Button disabled={connectionState !== 'OPEN'} onClick={() => send(new StopOrchestratorMessage(1))}>Send stop json</Button>
            </Form>

            <Form>
              <Button onClick={() => this.setState({ currentMessage: dequeue() })}>Dequeue</Button>
              <Button onClick={() => clearQueue()}>Clear queue</Button>
            </Form>

            {
              this.state.currentMessage && <div>
                <p>{JSON.stringify(this.state.currentMessage)}</p>
              </div>
            }
          </div>
        }
      </websocketContext.Consumer>
    )
  }
}