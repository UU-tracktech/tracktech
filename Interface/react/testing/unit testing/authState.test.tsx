/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import useAuthState from '../../src/classes/useAuthState'

//Tests which check the function returns the correct type
describe('state tests', () => {
  //basic loading check
  it('Returns loading while not initialized', () => {
    require('@react-keycloak/web').__SetMockInitialized(false)
    expect(useAuthState()).toBe('loading')
  })

  //State updates from loading to unauthenticated if not logged in
  it('Returns unauthenticated when loaded and not logged in', () => {
    //Start off with loading
    require('@react-keycloak/web').__SetMockInitialized(false)
    expect(useAuthState()).toBe('loading')

    //Update to simulate KC finishing loading and showing auth status
    require('@react-keycloak/web').__SetMockInitialized(true)
    require('@react-keycloak/web').__SetMockAuthenticated(false)
    expect(useAuthState()).toBe('unauthenticated')
  })

  //state updates from loading to authenticated when logged in
  it('Returns authenticated when loaded and logged in', () => {
    //Start as loading
    require('@react-keycloak/web').__SetMockInitialized(false)
    expect(useAuthState()).toBe('loading')

    //update to show a user is logged in
    require('@react-keycloak/web').__SetMockInitialized(true)
    require('@react-keycloak/web').__SetMockAuthenticated(true)
    expect(useAuthState()).toBe('authenticated')
  })
})
