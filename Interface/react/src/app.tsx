/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

/*
  App is the starting point of the React app
  This gets inserted into the DOM by index.tsx
*/

import React from 'react'
import { BrowserRouter, Route } from 'react-router-dom'
import { useKeycloak } from '@react-keycloak/web'
import { Layout } from 'antd'
import './app.less'

import { NavMenu } from './components/navbar'
import { NeedLogin } from './pages/needLogin'
import { Home } from './pages/home'
import { WebsocketProvider } from './components/websocketContext'
import useAuthState from './classes/useAuthState'

export function App() {
  const status = useAuthState()

  function body() {
    switch (status) {
      case 'loading':
        return <></>
      case 'unauthenticated':
        return <NeedLogin />
      case 'authenticated':
        return (
          <Route exact path="/">
            <Home />
          </Route>
        )
    }
  }

  return (
    <Layout
      style={{
        width: '100vw',
        height: '100vh',
        display: 'grid',
        gridTemplateRows: 'auto 1fr'
      }}
    >
      {/* Shows the navbar and page contents depending on user authentication */}
      <WebsocketProvider>
        <BrowserRouter key={1}>
          <NavMenu key={0} />
          {body()}
        </BrowserRouter>
      </WebsocketProvider>
    </Layout>
  )
}
