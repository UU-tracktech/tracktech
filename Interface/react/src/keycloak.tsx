/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import Keycloak from "keycloak-js";

const cfg = {
  //url: 'https://tracktech.ml:50009/auth/realms/Tracktech/protocol/openid-connect/auth',
  url: "https://tracktech.ml:50009/auth",
  realm: "Tracktech",
  clientId: "Interface",
};

const keycloak = Keycloak(cfg);

export default keycloak;
