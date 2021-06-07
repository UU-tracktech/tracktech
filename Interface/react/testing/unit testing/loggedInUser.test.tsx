/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { render, screen } from '@testing-library/react'
import { LoggedInUser } from '../../src/components/loggedInUser'
import '@testing-library/jest-dom'

//Most basic test, does it render at all?
test('Renders without error', () => {
  render(<LoggedInUser />)
})

//Test that it shows a skeleton while waiting for keycloak to load
test('Shows a skeleton while loading', () => {
  require('@react-keycloak/web').__SetMockInitialized(false)

  render(<LoggedInUser />)
  expect(screen.queryByTestId('loadingSkeleton')).toBeDefined()
})

//Test what is rendered when not logged in
test('render not logged in if not authenticated', () => {
  require('@react-keycloak/web').__SetMockInitialized(true)
  require('@react-keycloak/web').__SetMockAuthenticated(false)

  render(<LoggedInUser />)

  //We're not logged in, so we only expect the div meant for not being logged in to be there
  expect(screen.queryByTestId('notLoggedInDiv')).toBeDefined()
  expect(screen.queryByTestId('loggedInAsDiv')).toBeFalsy()
})

//Test what is rendered if a user is logged in
test('render username if authenticated', () => {
  require('@react-keycloak/web').__SetMockInitialized(true)
  require('@react-keycloak/web').__SetMockAuthenticated(true)
  let testName = 'Efawadh Aladeen'
  require('@react-keycloak/web').__SetMockTokenParsed({ name: testName })

  render(<LoggedInUser />)

  //We're logged in, so we only expect the div meant for being logged in to be there
  expect(screen.queryByTestId('notLoggedInDiv')).toBeFalsy()
  expect(screen.queryByTestId('loggedInAsDiv')).toBeDefined()
  expect(screen.queryByTestId('usernameText')).toBeDefined()

  //Check if the username of the user is displayed correctly
  expect(screen.getByTestId('loggedInAsDiv').innerHTML).toMatch('Logged in as:')
  expect(screen.getByTestId('usernameText').innerHTML).toMatch(testName)
})
