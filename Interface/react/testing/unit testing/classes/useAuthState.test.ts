/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

*/

import React from 'react'
import useAuthState from '../../../src/classes/useAuthState'

// Collection of tests that check each state individually and then combined
describe('Authentication state tests', () => {
  // Test the loading state
  it('Returns loading correctly', () => {
    require('@react-keycloak/web').__SetMockInitialized(false)
    expect(useAuthState()).toBe('loading')
  })

  // Test the unauthenticated state
  it('Returns unauthenticated correctly', () => {
    require('@react-keycloak/web').__SetMockInitialized(true)
    require('@react-keycloak/web').__SetMockAuthenticated(false)
    expect(useAuthState()).toBe('unauthenticated')
  })

  // Test the authenticated state
  it('Returns authenticated correctly', () => {
    require('@react-keycloak/web').__SetMockInitialized(true)
    require('@react-keycloak/web').__SetMockAuthenticated(true)
    expect(useAuthState()).toBe('authenticated')
  })

  // Test state changing based on keycloak
  it('Correctly changes based on the keycloak state', () => {
    // Page load, not initialized or logged in yet, expect state to be loading
    require('@react-keycloak/web').__SetMockInitialized(false)
    require('@react-keycloak/web').__SetMockAuthenticated(false)
    expect(useAuthState()).toBe('loading')

    // Finished loading but not logged in yet, expect unauthenticated
    require('@react-keycloak/web').__SetMockInitialized(true)
    expect(useAuthState()).toBe('unauthenticated')

    // User logged in, expect authenticated
    require('@react-keycloak/web').__SetMockAuthenticated(true)
    expect(useAuthState()).toBe('authenticated')
  })
})
