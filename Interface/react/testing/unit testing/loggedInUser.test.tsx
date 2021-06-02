/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { render, screen } from '@testing-library/react'
import { LoggedInUser } from '../../src/components/loggedInUser'
import '@testing-library/jest-dom'
import { useKeycloak } from '@react-keycloak/web'

jest.mock('useKeycloak')

/** Most basic test, does it render at all? */
test('Renders without error', () => {
  require('useKeycloak').__SetMockInitialized(true)
  render(<LoggedInUser />)
})

/** Test that it shows a skeleton while waiting for keycloak to load */
test.skip('Shows a skeleton while loading', () => {
  render(<LoggedInUser />)
  expect(screen.queryByTestId('loadingSkeleton')).toBeDefined()
})

/** Test what is rendered when not logged in */
test.skip('render not logged in if not authenticated', () => {
  render(<LoggedInUser />)

  //We're not logged in, so we only expect the div meant for not being logged in to be there
  expect(screen.queryByTestId('notLoggedInDiv')).toBeDefined()
  expect(screen.queryByTestId('loggedInAsDiv')).toBeFalsy()
})

/** Test what is rendered if a user is logged in */
test.skip('render username if authenticated', () => {
  render(<LoggedInUser />)

  //We're logged in, so we only expect the div meant for being logged in to be there
  expect(screen.queryByTestId('notLoggedInDiv')).toBeFalsy()
  expect(screen.queryByTestId('loggedInAsDiv')).toBeDefined()
  expect(screen.queryByTestId('usernameText')).toBeDefined()

  //Check if the username of the user is displayed correctly
  expect(screen.getByTestId('loggedInAsDiv').innerHTML).toMatch('Logged in as:')
  expect(screen.getByTestId('usernameText').innerHTML).toMatch(
    'Firstname Lastname'
  )
})
