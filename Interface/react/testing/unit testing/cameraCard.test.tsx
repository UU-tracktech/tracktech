/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
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

//Check if clicking the delete button calls the deletion function
test('Clicking delete calls delete function', () => {
  //Right now the delete function only shows an alert saying the delete button was pressed
  //So mock the alert so we can check if it was called
  const defaultAlert = window.alert //store the original alert
  const mockAlert = jest.fn()
  window.alert = mockAlert

  render(<CameraCard id={'0'} title={'title'} setSize={() => jest.fn()} />)

  //Check if the delete button exists
  const delButton = screen.queryByTestId('deleteButton')
  expect(delButton).toBeDefined

  //Simulate a click on the delete button and check if the function was called
  delButton?.click()
  expect(mockAlert).toBeCalled()

  //restore the normal alert
  window.alert = defaultAlert
})
