/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

*/

import React from 'react'
import { render, screen } from '@testing-library/react'
import {
  GetSegmentStarttime,
  PrintTimestamp,
  VideoPlayer
} from 'components/videojsPlayer'
import { Box } from 'classes/box'

let mockSnapCallback = jest.fn()
let mockOnTimestamp = jest.fn()
let mockOnPlayPause = jest.fn()
let mockOnPrimary = jest.fn()
let mockOnResize = jest.fn()

// Keep the log clean of videojs incompatible source errors
var consoleSpy: jest.SpyInstance
beforeAll(() => {
  consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {})
})
afterAll(() => {
  consoleSpy.mockRestore()
})

beforeEach(() => {
  render(
    <VideoPlayer
      setSnapCallback={mockSnapCallback}
      onTimestamp={mockOnTimestamp}
      onPlayPause={mockOnPlayPause}
      onPrimary={mockOnPrimary}
      onResize={mockOnResize}
      sources={[{ src: 'src' }]}
      autoplay={false}
    />
  )
})

// test if the callback functions passed as props get called
describe('prop tests', () => {
  it('Sets snapcallback and can take a screenshot', () => {
    expect(mockSnapCallback).toBeCalled()
    //obtain the function to take a screenshot
    let snapFunc = mockSnapCallback.mock.calls[0][0]
    //take a screenshot
    let snap = snapFunc(new Box(1, [2, 2, 4, 4], 'type'))
    expect(snap).toBeTruthy()
  })

  it('Calls onPrimary when clicking set primary button', async () => {
    while (screen.queryByText('Set primary') == null) {
      await new Promise((r) => setTimeout(r, 100))
    }
    screen.getByText('Set primary').click()
    expect(mockOnPrimary).toBeCalled()
  })
})

// Tests for the two timestamp functions used to calculate times from filenames
describe('Timestamp functions', () => {
  // Test if the timestamp is converted correctly
  it('PrintTimeStamp', () => {
    expect(PrintTimestamp(123.4)).toBe('2:03.4')
  })

  // Test if the function handles wrong names
  // and if the correct time is returned from a valid name
  it('GetSegmentStartTime', () => {
    let warnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {})

    // Wrong file extension test
    expect(GetSegmentStarttime('wrongtype.png', 2)).toBe(NaN)
    expect(warnSpy).toBeCalledWith(
      'GetSegmentStarttime: expected .ts file but got something else'
    )

    // No _V in the filename meaning it's probably not from our forwarder
    expect(GetSegmentStarttime('wrongname.ts', 2)).toBe(NaN)
    expect(warnSpy).toBeCalledWith('Video file not from forwarder')

    // Correct name, time obtained from 5 should be (5-1)*2 = 8
    expect(GetSegmentStarttime('file_V05.ts', 2)).toBe(8)
    warnSpy.mockRestore()
  })
})
