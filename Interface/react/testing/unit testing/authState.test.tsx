/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import useAuthState from '../../src/classes/useAuthState'

//Keycloak mock and variables to adjust the mock on a per test basis
var mockInitialized = false
var mockAuthenticated = false
jest.mock('@react-keycloak/web', () => {
  return {
    useKeycloak: () => ({
      initialized: mockInitialized,
      keycloak: {
        authenticated: mockAuthenticated
      }
    })
  }
})

/** Tests which check the function returns the correct type */
describe('state tests', () => {
  //basic loading check
  it('Returns loading while not initialized', () => {
    mockInitialized = false
    expect(useAuthState()).toBe('loading')
  })

  //State updates from loading to unauthenticated if not logged in
  it('Returns unauthenticated when loaded and not logged in', () => {
    mockInitialized = false
    expect(useAuthState()).toBe('loading')

    mockInitialized = true
    mockAuthenticated = false
    expect(useAuthState()).toBe('unauthenticated')
  })

  //state updates from loading to authenticated when logged in
  it('Returns authenticated when loaded and logged in', () => {
    mockInitialized = false
    expect(useAuthState()).toBe('loading')

    mockInitialized = true
    mockAuthenticated = true
    expect(useAuthState()).toBe('authenticated')
  })
})
