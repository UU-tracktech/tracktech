/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { screen, render, cleanup } from '@testing-library/react'
import {
  GetSegmentStarttime,
  PrintTimestamp,
  VideoPlayer
} from '../../src/components/videojsPlayer'
import { size } from '../../src/classes/size'

const mockOnTimestamp = jest.fn()
const mockOnResize = jest.fn((size: size) => {
  console.log(
    `w: ${size.width}, h: ${size.height}, l: ${size.left}, t: ${size.top}`
  )
})
const mockOnPrimary = jest.fn()
const mockOnPlayPause = jest.fn()

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

beforeEach(() => {
  render(
    <VideoPlayer
      onTimestamp={mockOnTimestamp}
      onResize={mockOnResize}
      onPrimary={mockOnPrimary}
      onPlayPause={mockOnPlayPause}
      setSnapCallback={() => undefined}
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
  //I highly doubt this can be tested since this is videojs stuff
  it.todo('onFirstplay') //would cover 67-69
  it.todo('onPlay') //would cover 75-78, and I assume onResize as well since it's called from onPlay
  it.todo('onPause') //would cover 85-87
})

describe('timestamp', () => {
  //not sure if this can ever be tested without taking these functions
  //outside of the videoplayer class and exporting them to make them public
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
