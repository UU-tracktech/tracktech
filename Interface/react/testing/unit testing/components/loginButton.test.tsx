/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

*/

import React from 'react'
import { screen, render } from '@testing-library/react'
import { LoginButton } from 'components/loginButton'
import { MockAuthProvider } from '../utilities/mockAuthContextProvider'

describe('Tests for the login button', () => {
  it('Shows skeleton while loading', () => {
    render(
      <MockAuthProvider state='loading'>
        <LoginButton />
      </MockAuthProvider>
    )

    expect(screen.queryByText('Login')).not.toBeTruthy()
    expect(screen.queryByText('Logout')).not.toBeTruthy()
  })

  it('Shows the login button if not logged in', () => {
    render(
      <MockAuthProvider state='unauthenticated'>
        <LoginButton />
      </MockAuthProvider>
    )

    expect(screen.queryByText('Login')).toBeTruthy()
  })

  it('Calls the login function when clicking login', () => {
    const mockLogin = jest.fn()
    render(
      <MockAuthProvider state='unauthenticated' login={mockLogin}>
        <LoginButton />
      </MockAuthProvider>
    )

    expect(screen.queryByText('Login')).toBeTruthy()
    screen.getByText('Login').click()

    expect(mockLogin).toBeCalled()
  })

  it('Shows the logout button if logged in', () => {
    render(
      <MockAuthProvider state='authenticated'>
        <LoginButton />
      </MockAuthProvider>
    )

    expect(screen.queryByText('Logout')).toBeTruthy()
  })

  it('Calls the logout function when clicking the logout button', () => {
    const mockLogout = jest.fn()

    render(
      <MockAuthProvider state='authenticated' logout={mockLogout}>
        <LoginButton />
      </MockAuthProvider>
    )

    expect(screen.queryByText('Logout')).toBeTruthy()
    screen.getByText('Logout').click()

    expect(mockLogout).toBeCalled()
  })
})
