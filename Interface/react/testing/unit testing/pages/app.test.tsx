/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

*/

import React from 'react'
import { render, screen } from '@testing-library/react'
import { App } from 'app'
import { act } from 'react-dom/test-utils'
import { fakeJWTToken } from '../utilities/mockAuthContextProvider'

// Tests to see if App displays the correct content based on keycloak status
describe('Test contents based on keycloak status', () => {
  // When not logged in it should show the login alert
  it('Shows login alert if not logged in', async () => {
    
    await act(async () => {
      render(<App />)
    })

    expect(screen.queryByTestId('loginAlert')).toBeTruthy()
  })

  // When logged in it doesn't show the other 2 which means it shows the correct content
  it('Shows home when logged in', async () => {
    
    global.localStorage.setItem('token', fakeJWTToken)

    await act(async () => {
      render(<App />)
    })

    expect(screen.queryByTestId('emptyWaitDiv')).not.toBeTruthy()
    expect(screen.queryByTestId('loginAlert')).not.toBeTruthy()
  })
})
