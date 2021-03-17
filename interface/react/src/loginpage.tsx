import React from 'react'

import { ReactKeycloakProvider } from "@react-keycloak/web";
import keycloak from './keycloak'

import LoginButton from "./components/LoginButton";

const eventLogger = (event, error) => {
    console.log('[Keycloak onEvent]', event, error)
}

const tokenLogger = (tokens) => {
    console.log('[Keycloak onTokens]', tokens)
}

const Loginpage = () => {

    return <ReactKeycloakProvider authClient={keycloak} onEvent={eventLogger} onTokens={tokenLogger}>

        <h1>Login pagina</h1>
        <LoginButton />

    </ReactKeycloakProvider>

}

export default Loginpage