import React, { Component } from 'react'

import { useKeycloak} from "@react-keycloak/web";

export const LoginButton = () => {

    const { keycloak, initialized } = useKeycloak();
    console.log('Keycloak connected: ', initialized);
    console.log('User authenticated: ', keycloak.authenticated);

    return(
        <div>
            {
                keycloak.authenticated ?
                    <button onClick={doLogout}>Logout</button> :
                    <button onClick={doLogin}>Login</button>
            }
        </div>
    )

    function doLogin() {
        keycloak.login();
    }

    function doLogout() {
        keycloak.logout();
    }
}

export default LoginButton



