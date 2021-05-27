/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

/**
  This component is the login button, which lets the user log in or out
  The functionality changes based on if the user is logged in or not
*/

import React from 'react'
import { Button, Skeleton } from 'antd'
import { useKeycloak } from '@react-keycloak/web'
import useAuthState from '../classes/useAuthState'

export function LoginButton() {
  //Obtain keycloak to look for login info
  const { keycloak } = useKeycloak()
  const status = useAuthState()

  //If the user is logged in, return a logout button
  //Otherwise return a login button
  switch (status) {
    case 'loading':
      return (
        <Skeleton.Button
          data-testid={'buttonSkeleton'}
          active
          style={{ verticalAlign: 'middle' }}
        />
      )
    case 'unauthenticated':
      return <Button onClick={() => keycloak.login()}>Login</Button>
    case 'authenticated':
      return <Button onClick={() => keycloak.logout()}>Logout</Button>
  }
}
