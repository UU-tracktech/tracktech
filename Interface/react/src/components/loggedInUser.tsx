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
import { Skeleton, Typography } from 'antd'
import { useKeycloak } from '@react-keycloak/web'
import useAuthState from '../classes/useAuthState'

export function LoggedInUser() {
  //Obtain keycloak so we can check for login info
  const { keycloak } = useKeycloak()

  const status = useAuthState()

  //If the user is logged in, obtain the username from the token and display it
  switch (status) {
    case 'loading':
      return (
        <Skeleton
          data-testid="loadingSkeleton"
          title={{ width: 150, style: { verticalAlign: 'middle' } }}
          paragraph={{
            rows: 1,
            width: 200,
            style: { margin: 0, verticalAlign: 'middle' }
          }}
          active
        />
      )
    case 'unauthenticated':
      return (
        <Typography.Text data-testid="notLoggedInDiv">
          You are currently not logged in
        </Typography.Text>
      )
    case 'authenticated':
      return (
        <div style={{ display: 'grid' }}>
          <Typography.Text
            data-testid="loggedInAsDiv"
            style={{ lineHeight: 3, color: 'rgb(153, 153, 153)' }}
          >
            Logged in as:
          </Typography.Text>
          <Typography.Text data-testid="usernameText" style={{ lineHeight: 0 }}>
            {keycloak.tokenParsed!['name']}
          </Typography.Text>
        </div>
      )
  }
}
