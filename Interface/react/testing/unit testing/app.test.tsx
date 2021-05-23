/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

/*

This test checks if app renders the needLogin page depending on 
user authentication

*/

import React from 'react'
import { act, getByRole, render, screen } from '@testing-library/react'
import { App } from '../../src/app'

//Mock values for the keycloak mock
let mockAuthenticated = false
let mockLogin = jest.fn()

//Keycloak mock
jest.mock('@react-keycloak/web', () => {
  return {
    useKeycloak: () => ({
      keycloak: {
        authenticated: mockAuthenticated,
        login: mockLogin
      }
    })
  }
})

/** Test to simply check if the page renders */
test('App renders without errors', async () => {
  await act(async () => {
    render(<App />)
  })
})

/** Test if the not logged in notification shows up when not authenticated */
test('shows login notification if not authenticated', async () => {
  await act(async () => {
    render(<App />)
  })

  expect(screen.queryByTestId('loginAlert')).not.toBe(null)
})

/** Test if closing the notification calls the close function which should call login */
test('redirects to login when closing notification', async () => {
  await act(async () => {
    render(<App />)
  })

  const alert = screen.getByTestId('loginAlert')
  const btn = getByRole(alert, 'button')

  expect(btn).toBeDefined

  btn.click()
  expect(mockLogin).toBeCalled()
})

/** Test to check if the page shows home when the user is authenticated */
test('shows home if authenticated', async () => {
  mockAuthenticated = true

  await act(async () => {
    render(<App />)
  })

  expect(screen.queryByTestId('loginAlert')).toBe(null)
})
