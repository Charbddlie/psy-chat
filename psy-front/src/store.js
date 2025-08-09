// src/store.js
import { createStore } from 'vuex'

export default createStore({
  state: {
    userInfo: {
      user_id: '',
      user_name: '',
    },
    chat_id: '',
    has_history: '',
    // 流程状态枚举
    flowStateEnum: {
      readInfo: 'readInfo',
      collectInfo: 'collectInfo',
      preTest: 'preTest',
      AIChat: 'AIChat',
      postTest: 'postTest',
      end: 'end',
      finalTest: 'finalTest',
      // endFinal: 'endFinal',
    },
    flowState: 'readInfo',
    skipStates: new Set(),
  },
  mutations: {
    setUserInfo(state, payload) {
      state.userInfo = { ...state.userInfo, ...payload }
    },
    setChatId(state, chat_id) {
      state.chat_id = chat_id;
    },
    setHasHistory(state, has_history) {
      state.has_history = has_history;
    },
    // 添加跳过的state
    addSkipState(state, skipState) {
      const debug = false
      if (debug) console.log('add skip:', skipState)
      if (debug) console.log('pre skip:', state.skipStates)
      if (!Object.values(state.flowStateEnum).includes(skipState)) return;
      state.skipStates.add(skipState);
      if (debug) console.log('post skip:', state.skipStates)
      if (debug) console.log('current flowState:', state.flowState)
      // 如果当前state已经在skipStates里，自动跳到下一个不在skipStates的state
      if (!state.skipStates.has(state.flowState)) return;

      if (debug) console.log('skip current flowState')
      // 直接实现setStateToNext的逻辑，延迟为0
      const states = Object.values(state.flowStateEnum);
      let idx = states.indexOf(state.flowState);
      if (idx !== -1 && idx < states.length - 1) {
        // 跳到下一个state，跳过skipStates中包含的state
        idx++;
        while (idx < states.length && state.skipStates.has(states[idx])) {
          idx++;
        }
        if (idx < states.length) {
          state.flowState = states[idx];
        }
      }
      if (debug) console.log('flowState:', state.flowState)
    },
    setStateToNext(state, { switchState, delay = 2000 }) {
      setTimeout(() => {
        const states = Object.values(state.flowStateEnum);
        let idx = states.indexOf(switchState);
        const cur_idx = states.indexOf(state.flowState);
        if (idx < cur_idx) return;
        // 如果当前state已经比申请切换的state要靠后，证明这个切换请求没必要执行
        if (idx !== -1 && idx < states.length - 1) {
          idx++;
          // 跳过skipStates中包含的state
          while (idx < states.length && state.skipStates.has(states[idx])) {
            idx++;
          }
          if (idx < states.length) {
            state.flowState = states[idx];
          }
        }
      }, delay);
    },
    setState(state, { newState, delay = 2000 }) {
      setTimeout(() => {
        const states = Object.values(state.flowStateEnum);
        let idx = states.indexOf(newState);
        // 跳过skipStates中包含的state
        while (idx !== -1 && idx < states.length && state.skipStates.has(states[idx])) {
          idx++;
        }
        if (idx !== -1 && idx < states.length) {
          state.flowState = states[idx];
        }
      }, delay)
    },
  }
})