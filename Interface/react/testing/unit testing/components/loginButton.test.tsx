/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

*/

import React from 'react'
import { screen, render } from '@testing-library/react'
import { LoginButton } from '../../../src/components/loginButton'

describe('Tests for the login button', () => {
  it('Shows skeleton while loading', () => {
    require('@react-keycloak/web').__SetMockInitialized(false)
    render(<LoginButton />)

    expect(screen.queryByText('Login')).not.toBeTruthy()
    expect(screen.queryByText('Logout')).not.toBeTruthy()
  })

  it('Shows the login button if not logged in', () => {
    require('@react-keycloak/web').__SetMockInitialized(true)
    require('@react-keycloak/web').__SetMockAuthenticated(false)
    render(<LoginButton />)

    expect(screen.queryByText('Login')).toBeTruthy()
  })

  it('Calls the login function when clicking login', () => {
    const mockLogin = jest.fn()

    require('@react-keycloak/web').__SetMockInitialized(true)
    require('@react-keycloak/web').__SetMockAuthenticated(false)
    require('@react-keycloak/web').__SetMockLoginFunction(mockLogin)
    render(<LoginButton />)

    expect(screen.queryByText('Login')).toBeTruthy()
    screen.getByText('Login').click()

    expect(mockLogin).toBeCalled()
  })

  it('Shows the logout button if logged in', () => {
    require('@react-keycloak/web').__SetMockInitialized(true)
    require('@react-keycloak/web').__SetMockAuthenticated(true)
    render(<LoginButton />)

    expect(screen.queryByText('Logout')).toBeTruthy()
  })

  it('Calls the logout function when clicking the logout button', () => {
    const mockLogout = jest.fn()

    require('@react-keycloak/web').__SetMockInitialized(true)
    require('@react-keycloak/web').__SetMockAuthenticated(true)
    require('@react-keycloak/web').__SetMockLogoutFunction(mockLogout)
    render(<LoginButton />)

    expect(screen.queryByText('Logout')).toBeTruthy()
    screen.getByText('Logout').click()

    expect(mockLogout).toBeCalled()
  })
})
