import Keycloak from 'keycloak-js'

/*
Om te gebruiken voor de daadwerkelijke website
Realm: Tracktech
Id: Interface
Auth: https://tracktech.ml:50009/auth/realms/Tracktech/protocol/openid-connect/auth
Token: https://tracktech.ml:50009/auth/realms/Tracktech/protocol/openid-connect/token
*/

const cfg = {
    //url: 'https://tracktech.ml:50009/auth/realms/Tracktech/protocol/openid-connect/auth',
    url: 'https://tracktech.ml:50009/auth',
    realm: 'Tracktech',
    clientId: 'Interface'
}

//Om te testen met een lokale keycloak server op localhost
// const cfg = {
//     url: 'http://localhost:8080/auth',
//     realm: 'Tracktech',
//     clientId: 'Interface'
// }

const keycloak = Keycloak(cfg)

export default keycloak