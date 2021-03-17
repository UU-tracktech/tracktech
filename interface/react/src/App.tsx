import React from 'react';
import './App.css';
import { BrowserRouter, Route } from 'react-router-dom'
import { Stream } from 'node:stream';
import Canvas1 from './components/CanvasTry'

import { NavMenu } from './components/navbar'
import { Home } from './pages/home'
import { Websocket } from './pages/websocket'
import { Logging } from './pages/logging'

type stream = { name: string, url: string, type: string }
type appState = { streams: stream[] }

class App extends React.Component<{}, appState> {

  render() {
    return (
      <div style={{width:"100%", height:"100vh"}} >
        <NavMenu key={0} />
        <BrowserRouter key={1}>
          <Route exact path='/' component={Home} />
          <Route path='/Websockets' component={Websocket} />
          <Route path='/Logging' component={Logging} />
        </BrowserRouter>
      </div>
    )
  }
}

export default App;