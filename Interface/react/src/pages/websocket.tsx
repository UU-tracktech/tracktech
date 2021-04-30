/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { Button, Form } from 'antd'

import {
  StartOrchestratorMessage,
  StopOrchestratorMessage,
  TestOrchestratorMessage
} from '../classes/orchestratorMessage'
import { websocketArgs, websocketContext } from '../components/websocketContext'

export function WebsocketUser() {
  return (
    <div>
      <websocketContext.Consumer>
        {({ send, setSocket, socketUrl, connectionState }: websocketArgs) => (
          <div>
            <p>URL: {socketUrl}</p>
            <p>STATE: {connectionState}</p>

            <Form>
              <Button
                onClick={() => setSocket('wss://tracktech.ml:50010/client2')}
              >
                Change Socket Url
              </Button>
              <Button
                disabled={connectionState !== 'OPEN'}
                onClick={() => send(new TestOrchestratorMessage('Test'))}
              >
                Send test json
              </Button>
              <Button
                disabled={connectionState !== 'OPEN'}
                onClick={() => send(new StartOrchestratorMessage('Test', 2, 3))}
              >
                Send start json
              </Button>
              <Button
                disabled={connectionState !== 'OPEN'}
                onClick={() => send(new StopOrchestratorMessage(1))}
              >
                Send stop json
              </Button>
            </Form>
          </div>
        )}
      </websocketContext.Consumer>
    </div>
  )
}
