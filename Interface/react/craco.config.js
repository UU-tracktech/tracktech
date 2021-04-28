const CracoLessPlugin = require('craco-less');

module.exports = {
  plugins: [
    {
      plugin: CracoLessPlugin,
      options: {
        lessLoaderOptions: {
          lessOptions: {
            modifyVars: { 
              '@primary-color': '#014584',
              '@error-color': '#ED1C24'
            },
            javascriptEnabled: true,
          },
        },
      },
    },
  ],
};