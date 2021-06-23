/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React, { useContext } from 'react'
import { BrowserRouter, Route } from 'react-router-dom'
import { Layout } from 'antd'
import './app.less'

import { NavMenu } from 'components/navbar'
import { NeedLogin } from 'pages/needLogin'
import { Home } from 'pages/home'
import { Timelines } from 'pages/timelines'
import { WebsocketProvider } from 'components/websocketContext'
import {
  environmentContext,
  EnvironmentProvider
} from 'components/environmentContext'
import { authContext, AuthProvider } from 'components/authContext'

const { Footer } = Layout

/**
 * Starting point of the React app, gets inserted into the DOM by index.tsx.
 * @returns The complete web application.
 */
export function App() {
  return (
    // Wrap the content in an enviroment provider to allow access to the enviroment settings from anywhere in the app.
    <EnvironmentProvider>
      <AuthorizedContent />
    </EnvironmentProvider>
  )

  /** Returns main content of the app, wrapped with an authorization provider */
  function AuthorizedContent() {
    const {
      clientId,
      accessTokenUri,
      authorizationUri,
      redirectUri
    } = useContext(environmentContext)

    return (
      <AuthProvider
        settings={{ clientId, accessTokenUri, authorizationUri, redirectUri }}
      >
        <Layout
          style={{
            width: '100vw',
            height: '100vh',
            display: 'grid',
            gridTemplateRows: 'auto 1fr'
          }}
        >
          {/* Shows the navbar and page contents depending on user authentication */}
          <BrowserRouter key={1}>
            <NavMenu key={0} />
            <Body />
            <Footer
              style={{
                position: 'static',
                height: 25,
                padding: '0px 0px 4px 0px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              © Utrecht University (ICS)
            </Footer>
          </BrowserRouter>
        </Layout>
      </AuthProvider>
    )
  }

  /**
   * Main body of the app.
   * @returns The content of the page body.
   */
  function Body() {
    const { status } = useContext(authContext)

    switch (status) {
      case 'loading':
        return <div data-testid={'emptyWaitDiv'} />
      case 'unauthenticated':
        return <NeedLogin />
      case 'authenticated':
      case 'no-auth':
        return (
          /* Wrap the main content in a websocket provider to provide the pages
           * with access to the websocket connection to the orchestrator. */
          <WebsocketProvider>
            <Route exact path='/'>
              <Home />
            </Route>
            <Route exact path='/timelines'>
              <Timelines />
            </Route>
          </WebsocketProvider>
        )
    }
  }
}
