/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { fireEvent, render, screen } from '@testing-library/react'
import { LoginButton } from '../../src/components/loginButton'

//Basic test to make sure the button renders
test('Button renders', () => {
  render(<LoginButton />)
})

test('Shows skeleton while loading', () => {
  require('@react-keycloak/web').__SetMockInitialized(false)

  render(<LoginButton />)

  expect(screen.queryByTestId('buttonSkeleton')).toBeDefined()
})

//Test to check if the button shows 'Login' and calls login function when not authenticated
test('Button to login', () => {
  require('@react-keycloak/web').__SetMockInitialized(true)
  require('@react-keycloak/web').__SetMockAuthenticated(false)
  let mockLogin = jest.fn()
  require('@react-keycloak/web').__SetMockLoginFunction(mockLogin)

  render(<LoginButton />)

  //We are not logged in so we expect there to be a button which says 'Login' and not one saying 'Logout'
  expect(screen.queryByText('Login')).toBeDefined()
  expect(screen.queryByText('Logout')).toBeFalsy()

  //simulate a click on the button
  fireEvent.click(screen.getByText('Login'))

  //after clicking the mock function used for login should have been called once
  expect(mockLogin).toBeCalled
  expect(mockLogin).toBeCalledTimes(1)
})

//Test to see if the content changes if a user is logged in
test('Button to logout', () => {
  require('@react-keycloak/web').__SetMockInitialized(true)
  require('@react-keycloak/web').__SetMockAuthenticated(true)
  let mockLogout = jest.fn()
  require('@react-keycloak/web').__SetMockLogoutFunction(mockLogout)

  render(<LoginButton />)

  //We are logged in so we expect there to be a button which says 'Logout' and not one saying 'Login'
  expect(screen.queryByText('Login')).toBeFalsy()
  expect(screen.queryByText('Logout')).toBeDefined()

  //simulate a click on the button
  fireEvent.click(screen.getByText('Logout'))

  //after clicking the mock function used for login should have been called once
  expect(mockLogout).toBeCalled
  expect(mockLogout).toBeCalledTimes(1)
})
