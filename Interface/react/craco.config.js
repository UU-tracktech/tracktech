const CracoLessPlugin = require('craco-less');

module.exports = {
  plugins: [
    {
      plugin: CracoLessPlugin,
      options: {
        lessLoaderOptions: {
          lessOptions: {
            modifyVars: { 
              '@primary-color': '#096dd9',
              '@error-color': '#cf1322'
            },
            javascriptEnabled: true,
          },
        },
      },
    },
  ],
};