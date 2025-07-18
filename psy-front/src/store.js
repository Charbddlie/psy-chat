// src/store.js
import { createStore } from 'vuex'

export default createStore({
  state: {
    userInfo: {
      id: '',
      name: '',
      age: ''
    }
  },
  mutations: {
    setUserInfo(state, payload) {
      state.userInfo = { ...state.userInfo, ...payload }
    }
  }
})