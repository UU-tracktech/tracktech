/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import * as React from 'react'
import { screen, render, cleanup } from '@testing-library/react'
import {
  GetSegmentStarttime,
  PrintTimestamp,
  VideoPlayer
} from '../../src/components/videojsPlayer'

const mockOnTimestamp = jest.fn()
const mockOnResize = jest.fn((w, h, l, t) => {
  console.log(`w: ${w}, h: ${h}, l: ${l}, t: ${t}`)
})
const mockOnPrimary = jest.fn()
const mockOnPlayPause = jest.fn()

beforeEach(() => {
  render(
    <VideoPlayer
      onTimestamp={mockOnTimestamp}
      onResize={mockOnResize}
      onPrimary={mockOnPrimary}
      onPlayPause={mockOnPlayPause}
    />
  )
})

afterEach(() => {
  cleanup()
})

test('It renders without error', () => {
  expect(screen.getByTestId('videojsplayer')).toBeDefined()
})

describe('callbacks', () => {
  it.todo('onFirstplay') //would cover 67-69
  it.todo('onPlay') //would cover 75-78, and I assume onResize as well since it's called from onPlay
  it.todo('onPause') //would cover 85-87
})

describe('timestamp', () => {
  it.todo('gets the segment name') //GetUri
  it.todo('Stores the first segment and looks for the next') //getInitialUri
  it.todo('calculates a timestamp from the 2nd segment') //LookForUriUpdate

  it('correctly calculates a time from a filename', () => {
    //Mock the console warning messages
    const warnSpy = jest
      .spyOn(global.console, 'warn')
      .mockImplementation(() => {})

    //Invalid format
    expect(GetSegmentStarttime('somenamewithoutextension')).toBe(NaN)
    expect(warnSpy).toBeCalledWith(
      'GetSegmentStarttime: expected .ts file but got something else'
    )

    warnSpy.mockClear() //clear data used for previous expect

    //Invalid naming
    expect(GetSegmentStarttime('nameWithoutunderscore.ts')).toBe(NaN)
    expect(warnSpy).toBeCalledWith('Video file not from forwarder')

    //Correct naming
    //V123 would mean segment 23, which is (23 - 1) * 2 = 44
    expect(GetSegmentStarttime('correct_V123.ts')).toBe(44)

    warnSpy.mockRestore()
  })

  it('Converts the timestamp in correct format', () => {
    expect(PrintTimestamp(54.6)).toBe('0:54.6') //test millisecond
    expect(PrintTimestamp(32)).toBe('0:32.0') //Test seconds
    expect(PrintTimestamp(65)).toBe('1:05.0') //Test minutes with seconds < 10
    expect(PrintTimestamp(876)).toBe('14:36.0') //Test minutes
  })
})
