/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React, { ReactNode, useState } from 'react'

/** Type for one setting's description of a camera. */
export type cameraSettingsType = {
  Name: string
  Id: string
  Forwarder: string
}

/** Type containing all the arguments needed to create a context containing the environment settings. */
export type environmentArgs = {
  cameras: cameraSettingsType[]
  objectTypes: string[]
  orchestratorWebsocketUrl: string
  orchestratorObjectIdsUrl: string
  orchestratorTimelinesUrl: string
  bufferTime: number
  segmentLength: number
  clientId: string
  accessTokenUri: string
  authorizationUri: string
  redirectUri: string
}

/** The context which can be used by other components to get settings from the environment settings file. */
export const environmentContext = React.createContext<environmentArgs>({
  cameras: [],
  objectTypes: [],
  // Dummy websocket since the url must be valid, but is expected to be changed later.
  orchestratorWebsocketUrl: 'wss://echo.websocket.org',
  orchestratorObjectIdsUrl: '',
  orchestratorTimelinesUrl: '',
  bufferTime: 10,
  segmentLength: 1,
  clientId: '',
  accessTokenUri: '',
  authorizationUri: '',
  redirectUri: ''
})

/** Context provider that reads settings file and serves results. */
export function EnvironmentProvider(props: { children: ReactNode }) {
  const [environment, setEnvironment] = useState<environmentArgs>()

  // Get settings and save them.
  React.useEffect(() => {
    try {
      fetch(process.env.PUBLIC_URL + '/settings.json').then((text) =>
        text.json().then((json) => {
          setEnvironment(json)
        })
      )
      // Catch fail as the settings file might be invalid.
    } catch {}
  }, [])

  return (
    <environmentContext.Provider
      value={{
        cameras: environment?.cameras ?? [],
        objectTypes: environment?.objectTypes ?? [],
        orchestratorWebsocketUrl: environment?.orchestratorWebsocketUrl ?? '',
        orchestratorObjectIdsUrl: environment?.orchestratorObjectIdsUrl ?? '',
        orchestratorTimelinesUrl: environment?.orchestratorTimelinesUrl ?? '',
        bufferTime: environment?.bufferTime ?? 10,
        segmentLength: environment?.segmentLength ?? 1,
        clientId: environment?.clientId ?? '',
        accessTokenUri: environment?.accessTokenUri ?? '',
        authorizationUri: environment?.authorizationUri ?? '',
        redirectUri: environment?.redirectUri ?? ''
      }}
    >
      {props.children}
    </environmentContext.Provider>
  )
}
