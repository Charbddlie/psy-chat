// const fs = require('fs');
const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
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