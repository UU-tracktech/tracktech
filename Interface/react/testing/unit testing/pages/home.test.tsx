/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

*/

import React from 'react'
import { getByText, queryByText, render, screen } from '@testing-library/react'
import { Home } from 'pages/home'
import '@testing-library/jest-dom'
import { environmentContext } from 'components/environmentContext'

// Test environment doesn't have an alert implementation
// Give it a temporary implementation to prevent warning during tests
var alertMock
beforeAll(() => {
  alertMock = jest.spyOn(global, 'alert').mockImplementation(() => {})
})

// Restore window alert
afterAll(() => {
  alertMock.mockClear()
})

// Setting for the test environment
const testTypes = ['Type1', 'Type2', 'Type3']
const testCams = [
  { Name: 'Cam1', Id: 'stream 1', Forwarder: 'url' },
  { Name: 'Cam2', Id: 'stream 2', Forwarder: 'url' }
]

// Render home with an environmentContext Provider to get content
beforeEach(() => {
  render(
    <environmentContext.Provider
      value={{
        cameras: testCams,
        objectTypes: testTypes,
        orchestratorWebsocketUrl: '',
        orchestratorObjectIdsUrl: '',
        orchestratorTimelinesUrl: '',
        bufferTime: 10,
        segmentLength: 2,
        clientId: '',
        accessTokenUri: '',
        authorizationUri: '',
        redirectUri: ''
      }}
    >
      <Home />
    </environmentContext.Provider>
  )
})

// Tests that check the indicator display mode
describe('Selection buttons', () => {
  it('Sets selection to All', () => {
    // Ensure the 3 buttons exist
    expect(screen.queryByTestId('AllButton')).toBeTruthy()

    let btn = screen.getByTestId('AllButton')
    btn.click()

    expect(btn).toHaveClass('ant-btn-primary')
    expect(btn).not.toHaveClass('ant-btn-default')
  })

  it('Sets selection to Selection', () => {
    expect(screen.queryByTestId('SelectionButton')).toBeTruthy()

    let btn = screen.getByTestId('SelectionButton')
    btn.click()

    expect(btn).toHaveClass('ant-btn-primary')
    expect(btn).not.toHaveClass('ant-btn-default')
  })

  it('Sets selection to None', () => {
    expect(screen.queryByTestId('NoneButton')).toBeTruthy()

    let btn = screen.getByTestId('NoneButton')
    btn.click()

    expect(btn).toHaveClass('ant-btn-primary')
    expect(btn).not.toHaveClass('ant-btn-default')
  })
})

// Tests that check the filter function
describe('ObjectTypeFilter tests', () => {
  it('Renders a button for each type', () => {
    expect(screen.queryAllByTestId('filterButton').length).toBe(
      testTypes.length
    )
  })

  it('Correctly toggles visibility', () => {
    let btn = screen.getAllByTestId('filterButton')[0]

    btn.click()
    expect(btn).toHaveClass('ant-btn-default')

    btn.click()
    expect(btn).toHaveClass('ant-btn-primary')
  })
})

// Test that checks the list of cameras
describe('Camera list tests', () => {
  it('Creates the camera list', () => {
    expect(screen.queryByText('Cameras')).toBeTruthy()
  })

  it('Creates an entry of each camera', () => {
    testCams.forEach((x) => {
      expect(screen.getByTestId(`camCard-${x.Id}`)).toBeTruthy()
    })
  })
})

//TODO: To increase coverage even more:
//TODO: Removing tracked objects
//TODO: Grid => SetPrimary
