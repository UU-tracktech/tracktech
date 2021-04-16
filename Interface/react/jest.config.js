module.exports = {
    moduleNameMapper: {
      '\\.(css|less)$': '<rootDir>/styleMock.js',
    },
    "automock": false,
    "setupFiles": [
      "<rootDir>/setupJest.js"
    ]
  };