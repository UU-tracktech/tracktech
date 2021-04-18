import * as React from 'react'
import { Navbar } from "react-bootstrap";
import { useKeycloak } from "@react-keycloak/web";

/**If a user is logged in, this will display the text "Signed in as: {username}" */
export const LoggedInUser = () => {

    //Obtain keycloak
    const { keycloak } = useKeycloak()

    return(
        <Navbar.Text>
            {
                keycloak.authenticated ? <>Hallo {getUsername()}</> : <></>
            }
        </Navbar.Text>
    )

    /**Returns the first name of the logged in user */
    function getUsername() : string {

        //The token contains all info we could need
        //First name, last name, email, etc
        if(keycloak.tokenParsed) {
            console.log('Token:', keycloak.tokenParsed)
            return keycloak.tokenParsed['given_name']
        }
        else
        {
            console.log('Can\'t get logged in user')
            return ''
        }
    }
}