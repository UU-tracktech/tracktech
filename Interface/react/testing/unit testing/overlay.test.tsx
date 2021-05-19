/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import * as React from 'react'
import { screen, render, cleanup } from '@testing-library/react'
import { Overlay } from '../../src/components/overlay'

const originalAlert = window.alert
beforeEach(() => {
  //replace alert implementation to prevent an error in the console
  window.alert = jest.fn((txt) => console.log('Alert: ' + txt))
})

afterEach(() => {
  window.alert = originalAlert //restore alert

  cleanup()
})

test('Renders without error', () => {
  render(
    <Overlay
      cameraId={'camID'}
      showBoxes={'All'}
      hiddenObjectTypes={[]}
      autoplay={false}
      onTimestamp={jest.fn()}
      onPlayPause={jest.fn()}
      onPrimary={jest.fn()}
      onResize={jest.fn()}
      sources={[
        {
          src:
            'http://sample.vodobox.com/big_buck_bunny_4k/big_buck_bunny_4k.m3u8',
          type: 'application/x-mpegURL'
        }
      ]}
    />
  )
  expect(screen.getByTestId('overlayDiv')).toBeDefined()
})

test('Renders without error showing only selection', () => {
  render(
    <Overlay
      cameraId={'camID'}
      showBoxes={'Selection'}
      hiddenObjectTypes={[]}
      autoplay={false}
      onTimestamp={jest.fn()}
      onPlayPause={jest.fn()}
      onPrimary={jest.fn()}
      onResize={jest.fn()}
      sources={[
        {
          src:
            'http://sample.vodobox.com/big_buck_bunny_4k/big_buck_bunny_4k.m3u8',
          type: 'application/x-mpegURL'
        }
      ]}
    />
  )
  expect(screen.getByTestId('overlayDiv')).toBeDefined()
})

test('Renders without error showing no indicators', () => {
  render(
    <Overlay
      cameraId={'camID'}
      showBoxes={'None'}
      hiddenObjectTypes={[]}
      autoplay={false}
      onTimestamp={jest.fn()}
      onPlayPause={jest.fn()}
      onPrimary={jest.fn()}
      onResize={jest.fn()}
      sources={[
        {
          src:
            'http://sample.vodobox.com/big_buck_bunny_4k/big_buck_bunny_4k.m3u8',
          type: 'application/x-mpegURL'
        }
      ]}
    />
  )
  expect(screen.getByTestId('overlayDiv')).toBeDefined()
})

test('Contains a videoPlayer', () => {
  render(
    <Overlay
      cameraId={'camID'}
      showBoxes={'All'}
      hiddenObjectTypes={[]}
      autoplay={false}
      onTimestamp={jest.fn()}
      onPlayPause={jest.fn()}
      onPrimary={jest.fn()}
      onResize={jest.fn()}
      sources={[
        {
          src:
            'http://sample.vodobox.com/big_buck_bunny_4k/big_buck_bunny_4k.m3u8',
          type: 'application/x-mpegURL'
        }
      ]}
    />
  )
  expect(screen.getByTestId('videojsplayer')).toBeDefined()
})
