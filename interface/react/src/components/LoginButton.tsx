import React from 'react'
import {Button, Navbar} from 'react-bootstrap'
import { useKeycloak} from "@react-keycloak/web";

/**This component shows a button, which when clicked either authorizes the user with keycloak
 * if not lgged in, and logs the user out if he is logged in */
export const LoginButton = () => {

    /*In order to have any keycloak functionality in a component,
      you have to use useKeycloak() */
    const { keycloak, initialized } = useKeycloak()
    console.log('Keycloak connected: ', initialized)
    console.log('User authenticated: ', keycloak.authenticated)

    /*Returns a button which either lets the user log in or out
    * depending on if they're authorized already or not */
    return(
        <div>
            {
                keycloak.authenticated ?
                    <Button onClick={doLogout}>Logout</Button>
                :
                    <Button onClick={doLogin}>Login</Button>
            }
        </div>
    )

    /**Call keycloak login */
    function doLogin() {
        keycloak.login()
    }

    /**Call keycloak logout */
    function doLogout() {
        keycloak.logout()
    }
}

export default LoginButton



