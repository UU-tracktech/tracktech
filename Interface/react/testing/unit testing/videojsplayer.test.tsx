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
