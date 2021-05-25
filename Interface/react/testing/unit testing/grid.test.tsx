/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import * as React from 'react'
import { render, screen } from '@testing-library/react'
import { Grid } from '../../src/components/grid'

it('renders without error', () => {
  render(
    <Grid
      primary="0"
      setPrimary={jest.fn}
      sources={[]}
      indicator={'All'}
      hiddenObjectTypes={[]}
    />
  )
})

//To stop some errors during testing, make an alert mock
var originalAlert
beforeAll(() => {
  //store the original alert to restore it later
  originalAlert = window.alert
  //replace the alert with a mock function that prints the alert to console
  window.alert = jest.fn((txt) => {
    console.log('Alert: ' + txt)
  })
})

afterAll(() => {
  //restore the alert
  window.alert = originalAlert
})

/** A list containing 3 made up sources to test with */
const mockSources = [
  {
    id: '0',
    name: 'source1',
    srcObject: { src: 'link', type: 'type' }
  },
  {
    id: '1',
    name: 'source2',
    srcObject: { src: 'link', type: 'type' }
  },
  {
    id: '2',
    name: 'source3',
    srcObject: { src: 'link', type: 'type' }
  }
]

it('number of elements match number of sources', () => {
  //temporarily replace the alert function with an empty function
  //This stops an error from appearing after a window.alert call in de overlay component
  //jest/jsdom does not imlement the alert function, therefore throwing an error when it's called
  const jsdomAlert = window.alert //keep a copy to restore it after the test
  window.alert = () => {}

  render(
    <Grid
      primary="0"
      setPrimary={jest.fn}
      sources={mockSources}
      indicator={'All'}
      hiddenObjectTypes={[]}
    />
  )

  //The grid contains an overlay for each VideoPlayer
  //There are 3 sources in the list, so there should be 3 overlays/videoplayers
  expect(screen.queryAllByTestId('gridElement').length).toBe(mockSources.length)

  //restore the alert function
  window.alert = jsdomAlert
})

/** Test to check the setPrimary function changes which video becomes primary */
it('Calls the setPrimary function', async () => {
  jest.setTimeout(30000)

  const mockFunc = jest.fn()

  render(
    <Grid
      primary="0"
      setPrimary={mockFunc}
      sources={mockSources}
      indicator={'All'}
      hiddenObjectTypes={[]}
    />
  )

  //wait fore the grid to load the video players
  while (screen.queryAllByText('Set primary').length == 0) {
    await new Promise((r) => setTimeout(r, 500))
  }

  //get the list of zoom buttons, length should equal number of sources
  const primaryButtonList = screen.getAllByText('Set primary')
  expect(primaryButtonList.length).toBe(mockSources.length)

  //simulate a click on zoom buttons and check if it called the function with correct args
  primaryButtonList[1].click()
  expect(mockFunc).toBeCalledTimes(1)
  expect(mockFunc).toBeCalledWith('1')

  primaryButtonList[2].click()
  expect(mockFunc).toBeCalledTimes(2)
  expect(mockFunc).toBeCalledWith('2')
})
