/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { Button } from 'react-bootstrap'
import { useKeycloak } from '@react-keycloak/web'

/**This component shows a button, which when clicked either authorizes the user with keycloak
 * if not logged in, and logs the user out if he is logged in */
export function LoginButton() {

  /*In order to have any keycloak functionality in a component,
    you have to use useKeycloak() */
  const { keycloak } = useKeycloak()

  /*Returns a button which either lets the user log in or out
  * depending on if they're authorized already or not */
  return (
    keycloak.authenticated
      ? <Button onClick={() => keycloak.logout()}>Logout</Button>
      : <Button onClick={() => keycloak.login()}>Login</Button>
  )
}



