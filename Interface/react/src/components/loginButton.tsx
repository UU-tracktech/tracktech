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
import { Button } from 'antd'
import { useKeycloak } from '@react-keycloak/web'

export function LoginButton() {
  //Obtain keycloak to look for login info
  const { keycloak } = useKeycloak()

  //If the user is logged in, return a logout button
  //Otherwise return a login button
  return keycloak.authenticated ? (
    <Button onClick={() => keycloak.logout()}>Logout</Button>
  ) : (
    <Button onClick={() => keycloak.login()}>Login</Button>
  )
}
