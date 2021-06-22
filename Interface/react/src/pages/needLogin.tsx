/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React, { useContext } from 'react'
import { Alert } from 'antd'
import { authContext } from 'components/authContext'

/**
 * This page shows up for any user that is not authenticated, to prevent
 * access to the video streams by unauthorized users.
 * @returns A screen displaying an error message signalling the user needs to log in.
 */
export function NeedLogin() {
  const { login } = useContext(authContext)
  return (
    <div
      data-testid={'loginAlert'}
      style={{
        display: 'grid',
        justifyContent: 'center',
        alignContent: 'center'
      }}
    >
      <Alert
        type={'error'}
        message={'Login'}
        description={'You need to be logged-in to view this page.'}
        onClose={() => login()}
        closable
      />
    </div>
  )
}
