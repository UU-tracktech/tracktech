/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

*/

import React from 'react'
import { render, screen } from '@testing-library/react'
import { SelectionCard } from 'components/selectionCard'

describe('Tests the properties of the selectionCard component', () => {
  // Test if the card gets the correct title and renders this title
  it('Gets the correct ID', () => {
    render(
      <SelectionCard objectId={6969} src={'someImg'} onClick={jest.fn()} />
    )

    expect(screen.queryByText('Object 6969')).toBeTruthy()
  })

  // Test if the image receives the given source
  it('Gets the correct image source', () => {
    render(
      <SelectionCard objectId={1} src={'imageSource'} onClick={jest.fn()} />
    )

    expect(screen.queryByTestId('image-imageSource')).toBeTruthy()
  })

  // Test if the delete function gets called
  it('Calls the onclick callback correctly', () => {
    let mockFunc = jest.fn()
    render(<SelectionCard objectId={1} src={'someImg'} onClick={mockFunc} />)

    // Click the delete button
    expect(screen.queryByTestId('deleteSelectionButton')).toBeTruthy()
    screen.getByTestId('deleteSelectionButton').click()

    // A confirmation should open, click yes to confirm
    expect(screen.queryByText('Yes')).toBeTruthy()
    screen.getByText('Yes').click()

    // Function should be called after confirmation
    expect(mockFunc).toBeCalled()
  })
})
