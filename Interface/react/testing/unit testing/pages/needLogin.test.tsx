/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

*/

import React from 'react'
import { render, screen } from '@testing-library/react'
import { NeedLogin } from 'pages/needLogin'
import { MockAuthProvider } from '../utilities/mockAuthContextProvider'

// Test if the login alert renders correctly
test('should show the login alert', () => {
  render(<NeedLogin />)
  expect(screen.queryByTestId('loginAlert')).toBeTruthy()
})

// Test if closing the alert by clicking on the X calls the login function
test('should call keycloak.login() on closing the alert', () => {
  let mockLogin = jest.fn()

  render(
    <MockAuthProvider state='unauthenticated' login={mockLogin}>
      <NeedLogin />
    </MockAuthProvider>
  )

  //There should be only 1 button on screen which is the close button
  screen.getByRole('button').click()
  expect(mockLogin).toBeCalled()
})
