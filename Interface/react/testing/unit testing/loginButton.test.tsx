import React from 'react'
import { fireEvent, render, screen } from '@testing-library/react'
import { LoginButton } from '../../src/components/loginButton'

//mock functions and values to change the keycloak mock per test
let mockAuthenticated = false
let mockLogin = jest.fn()
let mockLogout = jest.fn()

//mock the keycloak implementation
//https://stackoverflow.com/questions/63627652/testing-pages-secured-by-react-keycloak
jest.mock('@react-keycloak/web', () => {
  const originalModule = jest.requireActual('@react-keycloak/web')
  return {
    ...originalModule,
    useKeycloak: () => ({
      initialized: true,
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

/** Test to check if the button shows 'Login' and calls login function when not authenticated */
test('Button to login', () => {
  mockAuthenticated = false

  render(<LoginButton />)

  //We are not logged in so we expect there to be a button which says 'Login' and not one saying 'Logout'
  expect(screen.queryByText('Login')).not.toBe(null)
  expect(screen.queryByText('Logout')).toBe(null)

  //simulate a click on the button
  fireEvent.click(screen.getByText('Login'))

  //after clicking the mock function used for login should have been called once
  expect(mockLogin).toBeCalled
  expect(mockLogin).toBeCalledTimes(1)
})

/** Test to see if the content changes if a user is logged in */
test('Button to logout', () => {
  //change the mock to say we're logged in
  mockAuthenticated = true

  render(<LoginButton />)

  //We are logged in so we expect there to be a button which says 'Logout' and not one saying 'Login'
  expect(screen.queryByText('Login')).toBe(null)
  expect(screen.queryByText('Logout')).not.toBe(null)

  //simulate a click on the button
  fireEvent.click(screen.getByText('Logout'))

  //after clicking the mock function used for login should have been called once
  expect(mockLogout).toBeCalled
  expect(mockLogout).toBeCalledTimes(1)
})
