/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import { BrowserRouter, Route } from 'react-router-dom'

import { NavMenu } from './components/navbar'
import { Home } from './pages/home'
import { WebsocketUser } from './pages/websocket'
import { OverlayVideo } from './pages/overlayVideo'
import { WebsocketProvider } from './components/websocketContext'

export function App() {
  return (
    <div style={{ width: '100vw', height: '100vh', display: 'grid', gridTemplateRows: 'auto 1fr' }} >
      <WebsocketProvider>
        <BrowserRouter key={1}>
          <NavMenu key={0} />
          <Route exact path='/'><Home /></Route>
          <Route path='/Websockets'><WebsocketUser /></Route>
          <Route path='/Overlay'><OverlayVideo /></Route>
        </BrowserRouter>
      </WebsocketProvider>
    </div>
  )
}