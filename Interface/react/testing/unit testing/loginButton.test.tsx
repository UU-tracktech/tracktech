/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { fireEvent, render, screen } from '@testing-library/react'
import { LoginButton } from '../../src/components/loginButton'

//mock functions and values to change the keycloak mock per test
let mockInitialized = false
let mockAuthenticated = false
let mockLogin = jest.fn()
let mockLogout = jest.fn()

//mock the keycloak implementation
//https://stackoverflow.com/questions/63627652/testing-pages-secured-by-react-keycloak
jest.mock('@react-keycloak/web', () => {
  return {
    useKeycloak: () => ({
      initialized: mockInitialized,
      keycloak: {
        authenticated: mockAuthenticated,
        login: mockLogin,
        logout: mockLogout
      }
    })
  }
})

//Basic test to make sure the button renders
test('Button renders', () => {
  render(<LoginButton />)
})

test('Shows skeleton while loading', () => {
  mockInitialized = false

  render(<LoginButton />)

  expect(screen.queryByTestId('buttonSkeleton')).toBeDefined()
})

/** Test to check if the button shows 'Login' and calls login function when not authenticated */
test('Button to login', () => {
  mockInitialized = true
  mockAuthenticated = false

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

/** Test to see if the content changes if a user is logged in */
test('Button to logout', () => {
  //change the mock to say we're logged in
  mockInitialized = true
  mockAuthenticated = true

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
