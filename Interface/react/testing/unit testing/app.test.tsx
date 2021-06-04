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

test('App renders without errors', async () => {
  await act(async () => {
    render(<App />)
  })
})

//Start with testing what happens when keycloak has not finished loading yet
test('waits for keycloak to load before showing any contents', async () => {
  require('@react-keycloak/web').__SetMockInitialized(false)

  await act(async () => {
    render(<App />)
  })

  expect(screen.queryByTestId('emptyWaitDiv')).toBeDefined()
  expect(screen.queryByTestId('loginAlert')).toBeFalsy()
})

//Once keycloak is loaded and a user is not logged in it should show a login alert
test('shows login notification if not authenticated', async () => {
  jest.setTimeout(30000)

  //Configure the keycloak mock
  require('@react-keycloak/web').__SetMockInitialized(true)
  require('@react-keycloak/web').__SetMockAuthenticated(false)

  await act(async () => {
    render(<App />)
  })

  //Look for the login alert
  while (screen.queryByTestId('loginAlert') == null) {
    await new Promise((r) => setTimeout(r, 500))
  }
  expect(screen.queryByTestId('loginAlert')).toBeDefined()
})

//Closing the alert should call the login function
test('redirects to login when closing notification', async () => {
  jest.setTimeout(30000)

  //good practice to not rely on mock values still being there from a previous test
  //in case of a crash for example. Redo all values needed for the test
  require('@react-keycloak/web').__SetMockInitialized(true)
  require('@react-keycloak/web').__SetMockAuthenticated(false)
  //Also add a login function mock that we can check
  let mockLogin = jest.fn()
  require('@react-keycloak/web').__SetMockLoginFunction(mockLogin)

  await act(async () => {
    render(<App />)
  })

  //Get the alert, find the close button and close it
  while (screen.queryByTestId('loginAlert') == null) {
    await new Promise((r) => setTimeout(r, 500))
  }
  const alert = screen.getByTestId('loginAlert')
  const btn = getByRole(alert, 'button')
  expect(btn).toBeDefined()
  btn.click()

  //after clicking expect the login function to be called
  expect(mockLogin).toBeCalled()
})

//Test to check if the page shows home when the user is authenticated
test('shows home if authenticated', async () => {
  //Again, don't rely on values still being there, reset all required onces
  require('@react-keycloak/web').__SetMockInitialized(true)
  require('@react-keycloak/web').__SetMockAuthenticated(true)

  await act(async () => {
    render(<App />)
  })

  //Since we're logged in we expect the alert to not be there
  expect(screen.queryByTestId('loginAlert')).toBeFalsy()
})
