/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { useKeycloak } from '@react-keycloak/web'

export type authenticationState =
  | 'loading'
  | 'unauthenticated'
  | 'authenticated'

export default function useAuthState(): authenticationState {
  //Obtain keycloak so we can check for login info
  const { keycloak, initialized } = useKeycloak()

  //Return the current authentication state
  //return 'loading'
  return !initialized
    ? 'loading'
    : keycloak.authenticated
    ? 'authenticated'
    : 'unauthenticated'
}
