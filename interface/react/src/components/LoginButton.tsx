import React from 'react'

import { useKeycloak } from '@react-keycloak/web'

const LoginButton = () => {

    const { keycloak, initialized } = useKeycloak()

    {/*
    if(!initialized) {
        return <p>Loading keycloak...</p>
    }
    */}

    return (

        <div>
            {/*if the user is not logged in, show a login button*/}
            { keycloak && !keycloak.authenticated && <button onClick={()=>keycloak.login({redirectUri: 'https://oauth.pstmn.io/v1/callback'})}>Login</button> }
            {/*if the user IS logged in, show a logout button*/}
            { keycloak && keycloak.authenticated && <button onClick={()=>keycloak.logout()}>Logout</button>}
        </div>

    )
}

export default LoginButton