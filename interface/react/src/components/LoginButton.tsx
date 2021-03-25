import React from 'react'

import { useKeycloak} from "@react-keycloak/web";

const LoginButton = () => {

    const { keycloak, initialized } = useKeycloak();

    const login = () => {
        keycloak.login();
    }

    const logout = () => {
        keycloak.logout();
    }

    return (
      <div>

          <p>Keycloak {initialized ? '' : 'NOT' } connected</p>

          <p>User is {keycloak.authenticated ? '' : 'NOT' } authenticated</p>

          {
              keycloak.authenticated ?
                  <button onClick={logout}>Logout</button> :
                  <button onClick={login}>Login</button>
          }

      </div>
    );
}

export default LoginButton