/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

/**
 This component displays the login status
 If the user is logged in, it shows "Loggin in as: {username}"
 Otherwise, it shows "you are currently not logged in" 
*/

import React from 'react'
import { useKeycloak } from '@react-keycloak/web'

export function LoggedInUser() {
  //Obtain keycloak so we can check for login info
  const { keycloak } = useKeycloak()

  //If the user is logged in, obtain the username from the token and display it
  return keycloak.authenticated && keycloak.tokenParsed ? (
    <div>Logged in as: {keycloak.tokenParsed['name']}</div>
  ) : (
    <div>You are currently not logged in</div>
  )
}
