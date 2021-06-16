/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

module.exports = {
    moduleNameMapper: {
      '\\.(css|less)$': '<rootDir>/styleMock.js',
    },
    "automock": false,
    "setupFiles": [
      "<rootDir>/setupJest.js"
    ],
    "modulePaths": ["<rootDir>/react/src"]
  }