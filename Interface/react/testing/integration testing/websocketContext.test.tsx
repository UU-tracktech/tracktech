/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import { render, screen } from '@testing-library/react'
import React from 'react'
import {
  websocketArgs,
  websocketContext,
  WebsocketProvider
} from '../../src/components/websocketContext'
import { Overlay } from '../../src/components/overlay'

/**
 * Render a testing overlay which is used in all websocket tests
 */
beforeEach(() => {
  // Render a websocketprovider with an overlay to draw the bounding box.
  render(
    <WebsocketProvider>
      <div>
        <websocketContext.Consumer>
          {({ send, setSocket, socketUrl, connectionState }: websocketArgs) => (
            <>
              <Overlay
                cameraId="1"
                showBoxes={'All'}
                onTimestamp={() => {}}
                onPlayPause={() => {}}
                onPrimary={() => {}}
                onResize={() => {}}
                data-testId="overlay"
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
                data-testid="button"
                onClick={() => setSocket('ws://processor-orchestrator/client')}
              />
              <span data-testid="state">{connectionState}</span>
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
test.skip('Websocket connects', async () => {
  jest.setTimeout(30000)

  // Click the custom button to set the correct websocket
  screen.getByTestId('button').click()
  while (screen.getByTestId('state').textContent != 'OPEN') {
    await new Promise((r) => setTimeout(r, 500))
  }
  expect(screen.getByTestId('state').textContent).toBe('OPEN')
})

/**
 * Test whether or not an incoming bounding box is send to the queue and drawn.
 */
test.skip('Bounding box send to queue', async () => {
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
    boxes: [{ boxId: 1, rect: [0.2, 0.2, 0.8, 0.8], objectType: 'testObject' }]
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

  var boxesMessage = {
    type: 'boundingBoxes',
    frameId: 0,
    boxes: [{ boxId: 1, rect: [0.2, 0.2, 0.8, 0.8], objectType: 'testObject' }]
  }

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

  screen.getByTestId('box-1').click()

  while (screen.queryByTitle('startTrackButton') == null) {
    await new Promise((r) => setTimeout(r, 500))
  }

  expect(screen.getByTitle('startTrackButton')).toBeDefined()

  // Wait for message on processor
  while (!gotMessage) {
    await new Promise((r) => setTimeout(r, 500))
  }
  expect(gotMessage).toBeTruthy()
})
