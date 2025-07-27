import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import './assets/questionnaire.css'
import './assets/error.css'
import wsInstance from './tools.js'
wsInstance.connect();
import VueCookies from 'vue-cookies'
VueCookies.config('5min')

const app = createApp(App);
// app.provide('globalWS', wsInstance);
app.config.globalProperties.$ws = wsInstance;
app.config.globalProperties.$cookies = VueCookies;  // 将VueCookies挂载到全局
app.use(store);
app.mount('#app');
