import { Component } from 'react'
import { Button, Form, ListGroup } from 'react-bootstrap'

import { StartOrchestratorMessage, StopOrchestratorMessage, TestOrchestratorMessage } from '../classes/OrchestratorMessage'
import { Box } from '../classes/ClientMessage'
import { websocketArgs, websocketContext } from '../components/websocketContext'

type WebsocketUserState = { boxes: Box[] }
export class WebsocketUser extends Component<{}, WebsocketUserState> {

  static contextType = websocketContext;
  context!: React.ContextType<typeof websocketContext>;

  constructor(props: any) {
    super(props)
    this.state = { boxes: [] }
  }

  componentDidMount() {
    this.context.addListener(0, (boxes) => this.setState({ boxes: boxes }))
  }

  render() {
    return (<div>
      <websocketContext.Consumer>
        {
          ({ send, setSocket, socketUrl, connectionState }: websocketArgs) => <div>
            <p>URL: {socketUrl}</p>
            <p>STATE: {connectionState}</p>

            <Form>
              <Button onClick={() => setSocket('wss://tracktech.ml:50010/client')}>Change Socket Url</Button>
              <Button disabled={connectionState !== 'OPEN'} onClick={() => send(new TestOrchestratorMessage(1))}>Send test json</Button>
              <Button disabled={connectionState !== 'OPEN'} onClick={() => send(new StartOrchestratorMessage(1, 2, 3))}>Send start json</Button>
              <Button disabled={connectionState !== 'OPEN'} onClick={() => send(new StopOrchestratorMessage(1))}>Send stop json</Button>
            </Form>

            <ListGroup>
              {
                this.state.boxes.map((box: Box) => <ListGroup.Item>
                  {JSON.stringify(box)}
                </ListGroup.Item>)
              }
            </ListGroup>
          </div>
        }
      </websocketContext.Consumer>
    </div>
    )
  }
}