/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

*/

import React from 'react'
import { screen, render } from '@testing-library/react'
import { LoggedInUser } from 'components/loggedInUser'
import { MockAuthProvider, fakeJWTToken } from '../utilities/mockAuthContextProvider'

// Collection of tests to see if the component shows the correct thing based on the state
describe('State tests', () => {
  // Test if the skeleton is shown while waiting for keycloak to load
  it('Shows a skeleton while waiting for keycloak to load', () => {
    render(
      <MockAuthProvider state='loading'>
        <LoggedInUser />
      </MockAuthProvider>
    )

    expect(screen.queryByTestId('notLoggedInDiv')).not.toBeTruthy()
    expect(screen.queryByTestId('loggedInAsDiv')).not.toBeTruthy()
  })

  // Test if it shows a message saying the user is not logged in yet when loaded but not logged in
  it('Shows a not logged in message if not logged in', () => {
    render(
      <MockAuthProvider state='unauthenticated'>
        <LoggedInUser />
      </MockAuthProvider>
    )

    expect(screen.queryByTestId('notLoggedInDiv')).toBeTruthy()
  })

  // Test if it shows the username of the logged in user after logging in
  it('Shows the username if logged in', () => {
    render(
      <MockAuthProvider state='authenticated' token={fakeJWTToken}>
        <LoggedInUser />
      </MockAuthProvider>
    )

    expect(screen.queryByTestId('loggedInAsDiv')).toBeTruthy()
    expect(screen.queryByTestId('usernameText')).toBeTruthy()
    expect(screen.getByTestId('usernameText').innerHTML).toBe('John Doe')
  })

  // Test if the component updates correctly as the keycloak state changes
  it('Updates correctly according to state', () => {
    // Page load, not loaded and not logged in, expect skeleton
    const { rerender } = render(
      <MockAuthProvider state='loading'>
        <LoggedInUser />
      </MockAuthProvider>
    )
    expect(screen.queryByTestId('notLoggedInDiv')).not.toBeTruthy()
    expect(screen.queryByTestId('loggedInAsDiv')).not.toBeTruthy()

    // Finished loading but not logged in yet, expect not logged in message
    rerender(
      <MockAuthProvider state='unauthenticated'>
        <LoggedInUser />
      </MockAuthProvider>
    )
    expect(screen.queryByTestId('notLoggedInDiv')).toBeTruthy()

    rerender(
      <MockAuthProvider state='authenticated' token={fakeJWTToken}>
        <LoggedInUser />
      </MockAuthProvider>
    )
    expect(screen.queryByTestId('loggedInAsDiv')).toBeTruthy()
    expect(screen.queryByTestId('usernameText')).toBeTruthy()
    expect(screen.getByTestId('usernameText').innerHTML).toBe('John Doe')
  })
})
