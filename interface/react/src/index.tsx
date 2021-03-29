import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import './bootstrap.css'

import  { ReactKeycloakProvider } from "@react-keycloak/web";
import keycloak from "./keycloak";

//Writes keycloak events to the console for debugging
const keycloakEventLogger = (event, error) => {
    console.log('onKeycloakEvent:', event, error);
}

//Writes received tokens to the console for debugging
const keycloakTokenLogger = (tokens) => {
    console.log('onKeycloakToken:', tokens);
}

ReactDOM.render(
  <React.StrictMode>
      {/*App moet in de keycloakprovider gewikkeld worden om met keycloak te kunnen werken */}
      <ReactKeycloakProvider authClient={keycloak} onEvent={keycloakEventLogger} onTokens={keycloakTokenLogger}>
        <App />
      </ReactKeycloakProvider>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
