/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { Button, Skeleton } from 'antd'
import { useKeycloak } from '@react-keycloak/web'
import useAuthState from '../classes/useAuthState'

/**
 * Button allowing the user to log in or out, depending on authentication status.
 * @returns The login button.
 */
export function LoginButton() {
  // Obtain keycloak to look for login info.
  const { keycloak } = useKeycloak()
  const status = useAuthState()

  // If the user is logged in, return a logout button, otherwise return a login button.
  switch (status) {
    case 'loading':
      return <Skeleton.Button active style={{ verticalAlign: 'middle' }} />
    case 'unauthenticated':
      return <Button onClick={() => keycloak.login()}>Login</Button>
    case 'authenticated':
      return <Button onClick={() => keycloak.logout()}>Logout</Button>
  }
}
