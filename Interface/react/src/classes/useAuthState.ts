/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { useKeycloak } from '@react-keycloak/web'

/** Type enumerating the possible authentication states. */
export type authenticationState =
  | 'loading'
  | 'unauthenticated'
  | 'authenticated'

/**
 * Custom hook that wrappes the useKeyCloak hook.
 * @returns The current authentication state.
 */
export default function useAuthState(): authenticationState {
  // Obtain keycloak, to check for login info.
  const { keycloak, initialized } = useKeycloak()

  // Return the current authentication state.
  return !initialized
    ? 'loading'
    : keycloak.authenticated
    ? 'authenticated'
    : 'unauthenticated'
}
