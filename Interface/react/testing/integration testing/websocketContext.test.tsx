/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import { prettyDOM, render, screen, act } from '@testing-library/react'
import React from 'react'
import {
  websocketArgs,
  websocketContext,
  WebsocketProvider
} from 'components/websocketContext'
import { Overlay } from 'components/overlay'
import { StartOrchestratorMessage } from 'classes/orchestratorMessage'
import { BoxesClientMessage } from 'classes/clientMessage'
import { Box } from 'classes/box'

var websocketAddress

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
          {({ send, setSocket, connectionState, objects }: websocketArgs) => (
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
                hiddenObjectTypes={['hiddenObject']}
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
              <button
                data-testid='startWithImageButton'
                onClick={() =>
                  send(new StartOrchestratorMessage('2', 1, 1, 'testImage'))
                }
              />
              <span data-testid='selections'>
                {objects.map((obj) => (
                  <p data-testid={obj.image} />
                ))}
              </span>
            </>
          )}
        </websocketContext.Consumer>
      </div>
    </WebsocketProvider>
  )
})

/**
 * Test whether the interface is able to connect to the orchestrator using the websocket context provider.
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

  //set up a wrong socket url
  const originalAddress = websocketAddress
  websocketAddress = 'ws://wrong-address/test'

  //attempt connection
  screen.getByTestId('button').click()
  while (screen.getByTestId('state').textContent != 'CLOSED') {
    await new Promise((r) => setTimeout(r, 500))
  }

  //Check that the socket remains closed because it can't connect.
  expect(screen.getByTestId('state').textContent).toBe('CLOSED')

  //restore the original address for future tests
  websocketAddress = originalAddress
})

/**
 * Test whether an incoming bounding box is send to the queue and drawn.
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
test('Clicking Bounding boxes starts tracking', async () => {
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
      boxId: 1,
      image: 'data:image/png;base64,00'
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

/**
 * Test whether sending a start message with an image creates a selection box
 */
test('Start tracking with image creates selection', async () => {
  jest.setTimeout(30000)

  // Create a new websocket that will act as if it was a processor
  var processorSocket = new WebSocket('ws://processor-orchestrator/processor')
  while (processorSocket.readyState != 1) {
    await new Promise((r) => setTimeout(r, 500))
  }
  var identifyMessage = {
    type: 'identifier',
    id: '2'
  }
  processorSocket.send(JSON.stringify(identifyMessage))

  screen.getByTestId('button').click()
  while (screen.getByTestId('state').textContent != 'OPEN') {
    await new Promise((r) => setTimeout(r, 500))
  }

  // Send the start message
  screen.getByTestId('startWithImageButton').click()

  /* Now wait until the selection appears, the test environment maps selection 
  objects to paragraphs with a testid equal to the image value */
  while (screen.queryByTestId('testImage') == null) {
    await new Promise((r) => setTimeout(r, 500))
  }

  expect(screen.getByTestId('testImage')).toBeDefined()
})

test('Overlay only draws indicators specified by filters', async () => {
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

  //Send a box that has a type which gets filtered out
  var boxesMessage = new BoxesClientMessage('boundingBoxes', 0, [
    new Box(1, [0.2, 0.2, 0.8, 0.8], 'hiddenObject')
  ])

  screen.getByTestId('button').click()
  while (screen.getByTestId('state').textContent != 'OPEN') {
    await new Promise((r) => setTimeout(r, 500))
  }

  // Send the bounding boxes
  processorSocket.send(JSON.stringify(boxesMessage))
  //The box gets filtered out so it should not appear
  expect(screen.queryByTestId('box-1')).toBeFalsy()
})
