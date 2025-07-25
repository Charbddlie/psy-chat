// src/store.js
import { createStore } from 'vuex'

export default createStore({
  state: {
    userInfo: {
      userId: '',
      userName: '',
    },
    // 流程状态枚举
    flowStateEnum: {
      readInfo: 'readInfo',
      collectInfo: 'collectInfo',
      preTest: 'preTest',
      AIChat: 'AIChat',
      postTest: 'postTest',
      end: 'end',
    },
    flowState: 'postTest',
  },
  mutations: {
    setUserInfo(state, payload) {
      state.userInfo = { ...state.userInfo, ...payload }
    },
    setStateToNext(state, { currentState, delay = 2000 }) {
      const states = Object.values(state.flowStateEnum);
      const idx = states.indexOf(currentState);
      if (idx !== -1 && idx < states.length - 1) {
        setTimeout(() => {
          state.flowState = states[idx + 1];
        }, delay);
      }
    }
  }
})