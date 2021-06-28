/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

*/

import React from 'react'
import { screen, render } from '@testing-library/react'
import { CameraCard } from 'components/cameraCard'

describe('Collection of tests for the CameraCard', () => {
  it('Receives the correct ID', () => {
    render(<CameraCard id={'someID'} title={'cardTitle'} setSize={jest.fn()} />)
    expect(screen.queryByTestId('camCard-someID')).toBeDefined()
  })

  it('Sets the correct title', () => {
    render(<CameraCard id={'someID'} title={'cardTitle'} setSize={jest.fn()} />)
    expect(screen.queryByText('cardTitle')).toBeDefined()
  })

  it('Calls the resize function correctly', () => {
    let sizeFunc = jest.fn()
    render(<CameraCard id={'someID'} title={'cardTitle'} setSize={sizeFunc} />)
    expect(screen.queryByTestId('resizeButton')).toBeDefined()
    screen.getByTestId('resizeButton').click()
    expect(sizeFunc).toBeCalled()
    expect(sizeFunc).toBeCalledWith('someID')
  })
})
