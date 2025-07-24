import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import './assets/questionnaire.css'
import './assets/error.css'
import wsInstance from './tools.js'
wsInstance.connect();

const app = createApp(App);
// app.provide('globalWS', wsInstance);
app.config.globalProperties.$ws = wsInstance;
app.use(store);
app.mount('#app');
