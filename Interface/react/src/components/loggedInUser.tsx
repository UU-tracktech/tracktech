/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from "react";
import { useKeycloak } from "@react-keycloak/web";

/**If a user is logged in, this will display the text 'Signed in as: {username}' */
export function LoggedInUser() {
  //Obtain keycloak
  const { keycloak } = useKeycloak();

  return keycloak.authenticated && keycloak.tokenParsed ? (
    <div>Logged in as: {keycloak.tokenParsed["name"]}</div>
  ) : (
    <div>You are currently not logged in</div>
  );
}
