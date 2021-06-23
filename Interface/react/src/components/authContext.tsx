/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React, { ReactNode, useState } from 'react'
import ClientOauth2 from 'client-oauth2'
import jwt_decode from 'jwt-decode'

/** Type containing all the arguments needed to create a context authorization info and functionality. */
export type authArgs = {
  status: authenticationStatus
  login: () => void
  logout: () => void
  token: string
}

/** Type containing the required oauth2 settings. */
type authSettings = {
  clientId: string
  accessTokenUri: string
  authorizationUri: string
  redirectUri: string
}

/** Type enumerating the possible authentication states. */
export type authenticationStatus =
  | 'loading'
  | 'unauthenticated'
  | 'authenticated'
  | 'no-auth'

/** The context which can be used by other components to get auth data. */
export const authContext = React.createContext<authArgs>({
  status: 'unauthenticated',
  login: () => {},
  logout: () => {},
  token: ''
})

/** Context provider that gets authorization token. */
export function AuthProvider(props: {
  settings: authSettings
  children: ReactNode
}) {
  const [status, setStatus] = useState<authenticationStatus>('unauthenticated')
  const [token, setToken] = useState<string>()

  const client = new ClientOauth2({
    clientId: props.settings.clientId,
    accessTokenUri: props.settings.accessTokenUri,
    authorizationUri: props.settings.authorizationUri,
    redirectUri: props.settings.redirectUri
  })

  // Get auth settings and then the token from url.
  React.useEffect(() => {
    if (
      ![
        props.settings.accessTokenUri,
        props.settings.authorizationUri,
        props.settings.clientId,
        props.settings.redirectUri
      ].every((x) => x)
    ) {
      setStatus('no-auth')
      return
    } else if (status === 'no-auth') setStatus('unauthenticated')

    try {
      // If the callback was called from the authorization page, then the details are in the url.
      if (
        window.location.hash
          .split('&')
          .some((query) => query.startsWith('access_token')) ||
        window.location.search
          .split('&')
          .some((query) => query.startsWith('access_token'))
      ) {
        setStatus('loading')
        client.token.getToken(window.location).then((user) => {
          var token = user.accessToken

          var expired = hasExpired(token)

          if (!expired) {
            setToken(token)
            setStatus('authenticated')
            window.localStorage.setItem('token', token)
          } else {
            setToken('')
            setStatus('unauthenticated')
            window.localStorage.removeItem('token')
          }
        })

        // Replace the url so that the token can't be found in the history.
        window.history.replaceState(
          null,
          'TrackTech',
          props.settings.redirectUri
        )
        // If the url doesn't provide authorization info, check the local storage.
      } else if (window.localStorage.getItem('token')) {
        var token: string = window.localStorage.getItem('token') as string
        var expired = hasExpired(token)

        if (!expired) {
          setToken(token)
          setStatus('authenticated')
        } else {
          setToken('')
          setStatus('unauthenticated')
          window.localStorage.removeItem('token')
        }
      }

      // Catch fail in case the hash or search contained different parameters or if the settings file is incorrect.
    } catch {}
  }, [props.settings])

  /**
   * Helper function to check if a token has expired yet.
   * @param token The token to verify.
   */
  function hasExpired(token: string) {
    var decodedToken: any = jwt_decode(token)
    var expires: Date = new Date(0)
    expires.setUTCSeconds(decodedToken.exp)
    return expires < new Date()
  }

  /** Open a login page. */
  function login() {
    window.open(client.token.getUri(), '_self')
  }

  /** Delete login data and set user to be unauthenticated. */
  function logout() {
    setToken('')
    setStatus('unauthenticated')
    window.localStorage.removeItem('token')
  }

  return (
    <authContext.Provider
      value={{
        status: status,
        login: login,
        logout: logout,
        token: token ?? ''
      }}
    >
      {props.children}
    </authContext.Provider>
  )
}
