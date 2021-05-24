/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

/*
This page shows up for any user that is not authenticated, to prevent anyone from
being able to gain access to the video streams
*/

import React from 'react'
import { Alert } from 'antd'
import { useKeycloak } from '@react-keycloak/web'

export function NeedLogin() {
  const { keycloak } = useKeycloak()

  return (
    <div
      data-testid="loginAlert"
      style={{
        display: 'grid',
        justifyContent: 'center',
        alignContent: 'center'
      }}
    >
      <Alert
        type="error"
        message="Login"
        description="You need to be logged-in to view this page."
        onClose={() => keycloak.login()}
        closable
      />
    </div>
  )
}
