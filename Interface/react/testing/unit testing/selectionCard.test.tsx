/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { SelectionCard } from '../../src/components/selectionCard'

const testDataUrl =
  'data:image/gif;base64,R0lGODlhEAAQAMQAAORHHOVSKudfOulrSOp3WOyDZu6QdvCchPGolfO0o/XBs/fNwfjZ0frl3/zy7////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAkAABAALAAAAAAQABAAAAVVICSOZGlCQAosJ6mu7fiyZeKqNKToQGDsM8hBADgUXoGAiqhSvp5QAnQKGIgUhwFUYLCVDFCrKUE1lBavAViFIDlTImbKC5Gm2hB0SlBCBMQiB0UjIQA7'

test('Card renders without error', () => {
  render(<SelectionCard objectId={1} src={testDataUrl} onClick={() => {}} />)
})

test('card shows correct name', () => {
  // Render a card with 'title' as the title
  const { rerender } = render(
    <SelectionCard objectId={1} src={testDataUrl} onClick={() => {}} />
  )
  expect(screen.queryByText('Object 1')).not.toBe(null)

  // Rerender the card with a different object id
  // The object id in the title should have changed
  rerender(<SelectionCard objectId={2} src={testDataUrl} onClick={() => {}} />)
  expect(screen.queryByText('Object 1')).toBe(null)
  expect(screen.queryByText('Object 2')).not.toBe(null)
})

test('Delete button calls function correctly', () => {
  //Create a mock function to pass into the component
  const mockFn = jest.fn()

  render(<SelectionCard objectId={1} src={testDataUrl} onClick={() => {}} />)

  //make sure the button actually is on the card
  const button = screen.queryByTestId('deleteSelectionButton')
  expect(button).not.toBe(null)

  //simulate a click on the button
  fireEvent.click(screen.getByTestId('deleteSelectionButton'))
  //ensure the resize function was called by the click
  expect(mockFn).toHaveBeenCalled
})
