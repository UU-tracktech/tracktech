/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

*/

/*

This file contains the keycloak instance used to connect to our keycloak server
Keycloak is an identy provider used to provide login functionality

*/

import Keycloak from 'keycloak-js'

/** The configuration of the Keycloak instance */
const cfg = {
  url: 'https://tracktech.ml:50009/auth', //Link to the authentication server
  realm: 'Tracktech', //Which realm of the Keycloak server to use
  clientId: 'Interface' //Indication that we are the interface requesting authentication
}

/** The created keycloak instance using our configuration */
const keycloak = Keycloak(cfg)

export default keycloak
