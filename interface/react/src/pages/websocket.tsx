import React, { Component } from 'react'
import { Button, Form } from 'react-bootstrap'

import { StartOrchestratorMessage, StopOrchestratorMessage, TestOrchestratorMessage } from '../classes/orchestratorMessage'
import { Box } from '../classes/clientMessage'
import { websocketArgs, websocketContext } from '../components/websocketContext'

type WebsocketUserState = { boxes: Box[] }
export class WebsocketUser extends Component<{}, WebsocketUserState> {

  static contextType = websocketContext;
  context!: React.ContextType<typeof websocketContext>;

  constructor(props: any) {
    super(props)
    this.state = { boxes: [] }
  }

  render() {
    return (<div>
      <websocketContext.Consumer>
        {
          ({ send, setSocket, socketUrl, connectionState }: websocketArgs) => <div>
            <p>URL: {socketUrl}</p>
            <p>STATE: {connectionState}</p>

            <Form>
              <Button onClick={() => setSocket('wss://tracktech.ml:50010/client2')}>Change Socket Url</Button>
              <Button disabled={connectionState !== 'OPEN'} onClick={() => send(new TestOrchestratorMessage("Test"))}>Send test json</Button>
              <Button disabled={connectionState !== 'OPEN'} onClick={() => send(new StartOrchestratorMessage("Test", 2, 3))}>Send start json</Button>
              <Button disabled={connectionState !== 'OPEN'} onClick={() => send(new StopOrchestratorMessage(1))}>Send stop json</Button>
            </Form>
          </div>
        }
      </websocketContext.Consumer>
    </div>
    )
  }
}