/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import ReactDOM from 'react-dom'
import './index.css'
import { App } from './app'
import reportWebVitals from './reportWebVitals'
import './bootstrap.css'

import  { ReactKeycloakProvider } from "@react-keycloak/web";
import keycloak from "./keycloak";

/** Writes keycloak events to the console for debugging */
const keycloakEventLogger = (event, error) => {
    console.log('onKeycloakEvent:', event, error);
}

/** Writes received tokens to the console for debugging */
const keycloakTokenLogger = (tokens) => {
    console.log('onKeycloakToken:', tokens);
}

ReactDOM.render(
  <React.StrictMode>
      {/*The App has to be wrapped in <ReactKeycloakProvider in order to have any keycloak functionality */}
      <ReactKeycloakProvider authClient={keycloak} onEvent={keycloakEventLogger} onTokens={keycloakTokenLogger}>
        <App />
      </ReactKeycloakProvider>
  </React.StrictMode>,
  document.getElementById('root')
)

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals()
