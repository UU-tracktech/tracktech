import React from 'react'
import { BrowserRouter, Route } from 'react-router-dom'

import { NavMenu } from './components/navbar'
import { Home } from './pages/home'
import { WebsocketUser } from './pages/websocket'
import { OverlayVideo } from './pages/overlayVideo'
import { WebsocketProvider } from './components/websocketContext'


type stream = { name: string, url: string, type: string }
type appState = { streams: stream[] }

export class App extends React.Component<{}, appState> {
  render() {
    return (
      <div style={{ width: "100%", height: "100vh" }} >
        <WebsocketProvider>
          <BrowserRouter key={1}>
            <NavMenu key={0} />
            <Route exact path='/' ><Home /></Route>
            <Route path='/Websockets'  ><WebsocketUser /></Route>
            <Route path='/Overlay' ><OverlayVideo /></Route>
          </BrowserRouter>
        </WebsocketProvider>
      </div>
    )
  }
}