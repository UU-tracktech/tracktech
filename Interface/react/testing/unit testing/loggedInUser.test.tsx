/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { render, screen } from '@testing-library/react'
import { LoggedInUser } from '../../src/components/loggedInUser'
import '@testing-library/jest-dom'

//mock functions and values to change the keycloak mock per test
let mockAuthenticated = false
let mockToken = { name: 'Firstname Lastname' }

//mock the keycloak implementation
//https://stackoverflow.com/questions/63627652/testing-pages-secured-by-react-keycloak
jest.mock('@react-keycloak/web', () => {
  return {
    useKeycloak: () => ({
      keycloak: {
        authenticated: mockAuthenticated,
        tokenParsed: mockToken
      }
    })
  }
})

/** Most basic test, does it render at all? */
test('Renders the login status', () => {
  render(<LoggedInUser />)
})

/** Test what is rendered when not logged in */
test('render not logged in if not authenticated', () => {
  render(<LoggedInUser />)

  //We're not logged in, so we only expect the div meant for not being logged in to be there
  expect(screen.queryByTestId('notLoggedInDiv')).not.toBe(null)
  expect(screen.queryByTestId('loggedInAsDiv')).toBe(null)
})

/** Test what is rendered if a user is logged in */
test('render username if authenticated', () => {
  //Change the mock to say we're logged in
  mockAuthenticated = true

  render(<LoggedInUser />)

  //We're logged in, so we only expect the div meant for being logged in to be there
  expect(screen.queryByTestId('notLoggedInDiv')).toBe(null)
  expect(screen.queryByTestId('loggedInAsDiv')).not.toBe(null)

  //Check if the username of the user is displayed correctly
  expect(screen.queryByTestId('loggedInAsDiv')?.innerHTML).toMatch(
    'Logged in as: Firstname Lastname'
  )
})
