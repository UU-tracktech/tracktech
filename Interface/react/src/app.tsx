/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { BrowserRouter, Route } from 'react-router-dom'
import { Layout } from 'antd'
import './app.less'

import { NavMenu } from './components/navbar'
import { NeedLogin } from './pages/needLogin'
import { Home } from './pages/home'
import { Timelines } from './pages/timelines'
import { WebsocketProvider } from './components/websocketContext'
import { EnvironmentProvider } from './components/environmentContext'
import useAuthState from './classes/useAuthState'

/**
 * Starting point of the React app, gets inserted into the DOM by index.tsx.
 * @returns The complete web application.
 */
export function App() {
  const status = useAuthState()

  /**
   * Main body of the app.
   * @returns The content of the page body.
   */
  function body() {
    switch (status) {
      case 'loading':
        return <div data-testid={'emptyWaitDiv'}></div>
      case 'unauthenticated':
        return <NeedLogin />
      case 'authenticated':
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

  return (
    // Wrap the content in an enviroment provider to allow access to the enviroment settings from anywhere in the app.
    <EnvironmentProvider>
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
          {body()}
        </BrowserRouter>
      </Layout>
    </EnvironmentProvider>
  )
}
