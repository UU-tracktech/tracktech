/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import * as React from 'react'
import { screen, render, cleanup } from '@testing-library/react'
import { VideoPlayer } from '../../src/components/videojsPlayer'

beforeEach(() => {
  render(
    <VideoPlayer
      onTimestamp={jest.fn()}
      onResize={jest.fn()}
      onPrimary={jest.fn()}
      onPlayPause={jest.fn()}
    />
  )
})

afterEach(() => {
  cleanup()
})

test('It renders without error', () => {
  expect(screen.getByTestId('videojsplayer')).toBeDefined()
})

describe('videojs callbacks', () => {
  it.todo('onFirstplay')
  it.todo('onPlay')
  it.todo('onPause')
})

describe('timestamp', () => {
  it.todo('gets the segment name') //GetUri
  it.todo('Stores the first segment and looks for the next') //getInitialUri
  it.todo('calculates a timestamp from the 2nd segment') //LookForUriUpdate

  it.todo('correctly calculates a time from a filename') //getsegmentStartTime
  it.todo('Converts the timestamp in correct format') //PrintTimestamp
})

test.todo('Resizing')
