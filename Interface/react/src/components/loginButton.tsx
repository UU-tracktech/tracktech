/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React, { useContext } from 'react'
import { Button, Skeleton } from 'antd'
import { authContext } from 'components/authContext'

/**
 * Button allowing the user to log in or out, depending on authentication status.
 * @returns The login button.
 */
export function LoginButton() {
  // Obtain auth to look for login info.
  const { status, login, logout } = useContext(authContext)

  // If the user is logged in, return a logout button, otherwise return a login button.
  switch (status) {
    case 'no-auth':
      return <></>
    case 'loading':
      return <Skeleton.Button active style={{ verticalAlign: 'middle' }} />
    case 'unauthenticated':
      return <Button onClick={() => login()}>Login</Button>
    case 'authenticated':
      return <Button onClick={() => logout()}>Logout</Button>
  }
}
