import * as React from 'react'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { CameraCard } from '../../src/components/cameraCard'

test('Card renders without error', () => {
  render(<CameraCard id={'0'} title={'title'} setSize={() => {}} />)
})

test('card shows correct name', () => {
  //Render a card with 'title' as the title
  const { rerender } = render(
    <CameraCard id={'0'} title={'title'} setSize={() => {}} />
  )
  expect(screen.queryByText('title')).not.toBe(null)

  //rerender the card with 'different' as title.
  //'title' as title should be gone and now it should be 'different'
  rerender(<CameraCard id={'0'} title={'different'} setSize={() => {}} />)
  expect(screen.queryByText('title')).toBe(null)
  expect(screen.queryByText('different')).not.toBe(null)
})

test('size button calls function correctly', () => {
  //Create a mock function to pass into the component
  const mockFn = jest.fn()

  render(<CameraCard id={'0'} title={'title'} setSize={() => mockFn} />)

  //make sure the button actually is on the card
  const button = screen.queryByTestId('resizeButton')
  expect(button).not.toBe(null)

  //simulate a click on the button
  fireEvent.click(screen.getByTestId('resizeButton'))
  //ensure the resize function was called by the click
  expect(mockFn).toHaveBeenCalled
})

//TODO: once deleting is implemented, check if delete button removes card
test.todo('Clicking delete removes the card')
