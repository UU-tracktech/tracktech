/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import { Navbar } from 'react-bootstrap'
import { useKeycloak } from '@react-keycloak/web'

/**If a user is logged in, this will display the text 'Signed in as: {username}' */
export function LoggedInUser() {

  //Obtain keycloak
  const { keycloak } = useKeycloak()

  return (
    <div style={{ margin: '5px' }}>
      {
        keycloak.authenticated && keycloak.tokenParsed
          ? <Navbar.Text>Logged in as: {keycloak.tokenParsed['name']}</Navbar.Text>
          : <Navbar.Text>You are currently not logged in</Navbar.Text>
      }
    </div>
  )
}