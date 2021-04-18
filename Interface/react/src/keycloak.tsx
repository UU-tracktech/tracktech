import Keycloak from 'keycloak-js'

const cfg = {
    //url: 'https://tracktech.ml:50009/auth/realms/Tracktech/protocol/openid-connect/auth',
    url: 'https://tracktech.ml:50009/auth',
    realm: 'Tracktech',
    clientId: 'Interface'
}

const keycloak = Keycloak(cfg)

export default keycloak