/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

*/

import React from 'react'
import { screen, render } from '@testing-library/react'
import { ObjectCard } from 'components/objectCard'

// Collection of tests that check if the component correctly receives the properties
describe('ObjectCard property tests', () => {
  // Test if the ID properties is passed correctly
  it('Receives the correct ID', () => {
    render(<ObjectCard id={69} viewCallback={jest.fn()} />)

    expect(screen.queryByTestId('object-69')).toBeTruthy()
  })

  // Test if the callback function is passed and called correctly
  it('Calls the timeline function on click', () => {
    let mockCallback = jest.fn()
    render(<ObjectCard id={69} viewCallback={mockCallback} />)

    expect(screen.queryByTestId('objectViewButton')).toBeTruthy()
    screen.getByTestId('objectViewButton').click()

    expect(mockCallback).toBeCalled()
    expect(mockCallback).toBeCalledWith(69)
  })
})
