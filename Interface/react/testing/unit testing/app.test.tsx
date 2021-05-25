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
let mockInitialized = true
let mockAuthenticated = false
let mockLogin = jest.fn()

//Keycloak mock
jest.mock('@react-keycloak/web', () => {
  return {
    useKeycloak: () => ({
      initialized: mockInitialized,
      keycloak: {
        authenticated: mockAuthenticated,
        login: mockLogin,
        tokenParsed: { name: 'Firstname Lastname' }
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
  jest.setTimeout(30000)
  mockInitialized = true

  await act(async () => {
    render(<App />)
  })

  while (screen.queryByTestId('loginAlert') == null) {
    await new Promise((r) => setTimeout(r, 500))
  }

  expect(screen.queryByTestId('loginAlert')).toBeDefined()
})

/** Test if closing the notification calls the close function which should call login */
test('redirects to login when closing notification', async () => {
  jest.setTimeout(30000)
  mockInitialized = true

  await act(async () => {
    render(<App />)
  })

  while (screen.queryByTestId('loginAlert') == null) {
    await new Promise((r) => setTimeout(r, 500))
  }

  const alert = screen.getByTestId('loginAlert')
  const btn = getByRole(alert, 'button')

  expect(btn).toBeDefined()

  btn.click()
  expect(mockLogin).toBeCalled()
})

/** Test to check if the page shows home when the user is authenticated */
test('shows home if authenticated', async () => {
  mockInitialized = true
  mockAuthenticated = true

  await act(async () => {
    render(<App />)
  })

  expect(screen.queryByTestId('loginAlert')).toBeFalsy()
})

test('waits for keycloak to load before showing any contents', async () => {
  mockInitialized = false

  await act(async () => {
    render(<App />)
  })

  expect(screen.queryByTestId('emptyWaitDiv')).toBeDefined()
  expect(screen.queryByTestId('loginAlert')).toBeFalsy()
})
