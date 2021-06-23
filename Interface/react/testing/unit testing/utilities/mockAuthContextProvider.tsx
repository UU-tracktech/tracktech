import React, { ReactNode } from 'react'
import { authContext, authenticationStatus } from 'components/authContext'

/** JWT token generated at http://jwtbuilder.jamiekurtz.com/ with name John Doe */
export const fakeJWTToken =
  'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE2MjQyODYwNDksImV4cCI6MTY1NTgyMjA0OSwiYXVkIjoid3d3LnRyYWNrdGVjaC5tbCIsInN1YiI6Impkb2VAdHJhY2t0ZWNoLmNvbSIsIkdpdmVuTmFtZSI6IkpvaG4iLCJTdXJuYW1lIjoiRG9lIiwiRW1haWwiOiJqZG9lQHRyYWNrdGVjaC5jb20iLCJuYW1lIjoiSm9obiBEb2UifQ.-0fJ6inMOUiLASSsT_2lheo3e5qHsYhZoQihKDyy4aY'

/** Mock context provider that can be configured to provide mocked authentication data. */
export function MockAuthProvider(props: {
    children: ReactNode,
    state?: authenticationStatus,
    token?: string,
    login?: () => void,
    logout?: () => void
  }) {
  
    return (
      <authContext.Provider
        value={{
          status: props.state ?? 'unauthenticated',
          login: props.login ?? (() => {}),
          logout: props.logout ?? (() => {}),
          token: props.token ?? ''
        }}
      >
        {props.children}
      </authContext.Provider>
    )
  }