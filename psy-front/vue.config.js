// const fs = require('fs');
const { defineConfig } = require('@vue/cli-service');
const webpack = require('webpack');

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: 'false'
      })
    ]
  },
  // devServer: {
  //   server: {
  //     type: 'https',
  //     options: {
  //       key: fs.readFileSync('./certs/localhost-key.pem'),
  //       cert: fs.readFileSync('./certs/localhost.pem'),
  //     }
  //   },
  //   port: 8080,
  // }
});