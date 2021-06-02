/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import { prettyDOM, render, screen } from '@testing-library/react'
import React from 'react'
import {
  websocketArgs,
  websocketContext,
  WebsocketProvider
} from '../../src/components/websocketContext'
import { Overlay } from '../../src/components/overlay'
import { StartOrchestratorMessage } from '../../src/classes/orchestratorMessage'
import { Box, BoxesClientMessage } from '../../src/classes/clientMessage'

var websocketAddress

//mock functions and values to change the keycloak mock per test
let mockInitialized = true
let mockAuthenticated = false
let mockToken = { name: 'Firstname Lastname' }

//mock the keycloak implementation
//https://stackoverflow.com/questions/63627652/testing-pages-secured-by-react-keycloak
jest.mock('@react-keycloak/web', () => {
  return {
    useKeycloak: () => ({
      initialized: mockInitialized,
      keycloak: {
        authenticated: mockAuthenticated,
        tokenParsed: mockToken
      }
    })
  }
})

/**
 * Render a testing overlay which is used in all websocket tests
 */
beforeEach(() => {
  //reset the correct link just in case a test which changes it crashes
  websocketAddress = 'ws://processor-orchestrator/client'

  // Render a websocketprovider with an overlay to draw the bounding box.
  render(
    <WebsocketProvider>
      <div>
        <websocketContext.Consumer>
          {({ send, setSocket, socketUrl, connectionState }: websocketArgs) => (
            <>
              <Overlay
                source={{
                  id: '1',
                  name: 'name',
                  srcObject: { src: 'src', type: 'type' }
                }}
                showBoxes={'All'}
                onPrimary={() => {}}
                data-testId='overlay'
                hiddenObjectTypes={[]}
                sources={[
                  {
                    src:
                      'http://sample.vodobox.com/big_buck_bunny_4k/big_buck_bunny_4k.m3u8',
                    type: 'application/x-mpegURL'
                  }
                ]}
                autoplay={true}
              ></Overlay>
              <button
                data-testid='button'
                onClick={() => setSocket(websocketAddress)}
              />
              <span data-testid='state'>{connectionState}</span>
            </>
          )}
        </websocketContext.Consumer>
      </div>
    </WebsocketProvider>
  )
})

/**
 * Test whether or not the interface is able to connect to the orchestrator using the websocket context provider.
 */
test('Websocket connects', async () => {
  jest.setTimeout(30000)

  // Click the custom button to set the correct websocket
  screen.getByTestId('button').click()
  while (screen.getByTestId('state').textContent != 'OPEN') {
    await new Promise((r) => setTimeout(r, 500))
  }
  expect(screen.getByTestId('state').textContent).toBe('OPEN')
})

/** Test whether the websocket correctly handles a wrong url */
test('Websocket handles error and closes', async () => {
  jest.setTimeout(30000)
  const msgSpy = jest.spyOn(global.console, 'log')

  //set up a wrong socket url
  const originalAddress = websocketAddress
  websocketAddress = 'ws://wrong-address/test'

  //attempt connection
  screen.getByTestId('button').click()
  while (screen.getByTestId('state').textContent != 'CLOSED') {
    await new Promise((r) => setTimeout(r, 500))
  }

  //since the state changes quickly I rely on a message in the console to confirm
  //the websocket went through the error function
  expect(msgSpy).toBeCalledWith('socket error')

  //Confirm the socket is closed
  expect(msgSpy).toBeCalledWith('closed socket')
  expect(screen.getByTestId('state').textContent).toBe('CLOSED')

  //restore the original address for future tests
  websocketAddress = originalAddress
})

/**
 * Test whether or not an incoming bounding box is send to the queue and drawn.
 */
test('Bounding box send to queue', async () => {
  jest.setTimeout(30000)

  // Create a new websocket that will act as if it was a processor
  var processorSocket = new WebSocket('ws://processor-orchestrator/processor')
  while (processorSocket.readyState != 1) {
    await new Promise((r) => setTimeout(r, 500))
  }
  var identifyMessage = {
    type: 'identifier',
    id: '1'
  }
  processorSocket.send(JSON.stringify(identifyMessage))

  screen.getByTestId('button').click()
  while (screen.getByTestId('state').textContent != 'OPEN') {
    await new Promise((r) => setTimeout(r, 500))
  }

  var boxesMessage = {
    type: 'boundingBoxes',
    frameId: 0,
    boxes: [new Box(1, [0.2, 0.2, 0.8, 0.8], 'testObject')]
  }

  // Send the bounding boxes
  processorSocket.send(JSON.stringify(boxesMessage))
  while (screen.queryByTestId('box-1') == null) {
    await new Promise((r) => setTimeout(r, 500))
  }

  expect(screen.getByTestId('box-1')).toBeDefined()
})

/**
 * Test whether clicking on the box will result in a start command going to the processor
 */
test('Bounding boxes start tracking', async () => {
  jest.setTimeout(30000)

  // Create a new websocket that will act as if it was a processor
  var processorSocket = new WebSocket('ws://processor-orchestrator/processor')
  while (processorSocket.readyState != 1) {
    await new Promise((r) => setTimeout(r, 500))
  }
  var identifyMessage = {
    type: 'identifier',
    id: '1'
  }
  processorSocket.send(JSON.stringify(identifyMessage))

  var boxesMessage = new BoxesClientMessage('boundingBoxes', 0, [
    new Box(1, [0.2, 0.2, 0.8, 0.8], 'testObject')
  ])

  screen.getByTestId('button').click()
  while (screen.getByTestId('state').textContent != 'OPEN') {
    await new Promise((r) => setTimeout(r, 500))
  }

  // Send the bounding boxes
  processorSocket.send(JSON.stringify(boxesMessage))
  while (screen.queryByTestId('box-1') == null) {
    await new Promise((r) => setTimeout(r, 500))
  }

  expect(screen.getByTestId('box-1')).toBeDefined()

  var gotMessage = false

  // Set up processor assert for when the message comes in
  processorSocket.onmessage = (ev: MessageEvent<any>) => {
    expect(JSON.parse(ev.data)).toStrictEqual({
      type: 'start',
      objectId: 1,
      frameId: 0,
      boxId: 1
    })
    gotMessage = true
  }

  //Get the drawn bounding box and click to start tracking
  const box = screen.getByTestId('box-1')
  box.click()

  //wait for the confirmation popup
  while (screen.queryAllByText('OK').length == 0) {
    await new Promise((r) => setTimeout(r, 500))
  }

  //get the confirm button, make sure it exists, then press the button
  const confirmButton = screen.getByText('OK')
  expect(confirmButton).toBeDefined()
  confirmButton.click()

  // Wait for message on processor
  while (!gotMessage) {
    await new Promise((r) => setTimeout(r, 500))
  }
  expect(gotMessage).toBeTruthy()
})

test.todo('Clicking tracked object indicator stops tracking')

test.todo('Overlay only draws indicators specified by filters')
