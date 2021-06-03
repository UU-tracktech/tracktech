/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

*/

//Custom functions that the tests can use to set certain values of the mock
//initialized
let mockInitialized = false
/** Set the value returned in the { initialized } by useKeycloak
 * @param {boolean} newMockval The boolean value to return
 */
export function __SetMockInitialized(newMockval) {
  mockInitialized = newMockval
}

//authenticated
let mockAuthenticated = false
/** Set the value returned in keycloak.authenticated
 * @param {boolean} newMockval The boolean value to return
 */
export function __SetMockAuthenticated(newMockval) {
  mockAuthenticated = newMockval
}

//token
let mockToken = {}
/**
 * Set the values returned in keycloak.tokenParsed. At least a "name" entry is recommeded
 * @param {object} newMockToken The token contents to return
 * @example { name: 'John Doe' }
 */
export function __SetMockTokenParsed(newMockToken) {
  mockToken = newMockToken
}

//login
let mockLoginFn = jest.fn()
/**
 * Set the function that is called when calling keycloak.login()
 * @param {function} func The function to call on login
 */
export function __SetMockLoginFunction(func) {
  mockLoginFn = func
}

//logout
let mockLogoutFn = jest.fn()
/**
 * Set the function that us called when calling keycloak.logout()
 * @param {function} func The function to call on logout
 */
export function __SetMockLogoutFunction(func) {
  mockLogoutFn = func
}

//Custom version of 'useKeycloak' function
export function useKeycloak() {
  return {
    initialized: mockInitialized,
    keycloak: {
      authenticated: mockAuthenticated,
      tokenParsed: mockToken,
      login: mockLoginFn,
      logout: mockLogoutFn
    }
  }
}
