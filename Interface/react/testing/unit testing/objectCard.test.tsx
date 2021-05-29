/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import * as React from 'react'
import { fireEvent, render, screen } from '@testing-library/react'
import { ObjectCard } from '../../src/components/objectCard'

test('Object card renders without error', () => {
  render(<ObjectCard id={0} viewCallback={() => {}} />)
})

test('object card shows correct title', () => {
  //Render a card with object id 0
  const { rerender } = render(<ObjectCard id={0} viewCallback={() => {}} />)
  // Expect the title to be set correctly
  expect(screen.queryByText('Object 0')).not.toBe(null)

  //rerender the card with a different id.
  //expect the title to have updated
  rerender(<ObjectCard id={1} viewCallback={() => {}} />)
  expect(screen.queryByText('Object 0')).toBe(null)
  expect(screen.queryByText('Object 1')).not.toBe(null)
})

test('View button calls function correctly', () => {
  //Create a mock function to pass into the component
  const mockFn = jest.fn()

  render(<ObjectCard id={0} viewCallback={(id) => mockFn(id)} />)

  //make sure the button actually is on the card
  const button = screen.queryByTestId('objectViewButton')
  expect(button).not.toBe(null)

  //simulate a click on the button
  fireEvent.click(screen.getByTestId('objectViewButton'))
  //ensure the resize function was called by the click
  expect(mockFn).toHaveBeenCalledWith(0)
})
