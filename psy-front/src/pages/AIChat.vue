<template>
  <div class="ai-chat-container">
    <!-- 错误弹窗 -->
    <transition name="fade">
      <div v-if="errorMessage" class="error-modal">
        <div class="error-modal-content">
          <span class="error-modal-close" @click="errorMessage = ''">&times;</span>
          <div class="error-modal-icon">⚠️</div>
          <div class="error-modal-text">{{ errorMessage }}</div>
        </div>
      </div>
    </transition>
    <!-- 跳转弹窗 -->
    <transition name="fade">
      <div v-if="endFlag" class="error-modal">
        <div class="error-modal-content">
          <span class="error-modal-close">&times;</span>
          <div class="error-modal-icon">🥰</div>
          <div class="error-modal-text">聊天结束啦</div>
        </div>
      </div>
    </transition>
    <div class="chat-messages" ref="messageContainer">
      <transition-group name="bubble" tag="div">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="['message', message.isUser ? 'user-message' : 'ai-message']"
        >
          <div class="avatar" v-if="!message.isUser">
            <img src="/favicon.ico" alt="AI" class="AI-img"/>
          </div>
          <div class="message-content">
            {{ message.content }}
          </div>
          <div class="avatar" v-if="message.isUser">
            <span>🧑</span>
          </div>
        </div>
      </transition-group>
      <div v-if="loading" class="message ai-message">
        <div class="avatar"><img src="/favicon.ico" alt="AI" class="AI-img"/></div>
        <div class="message-content loading">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
          <span style="margin-left:8px;">AI 正在思考...</span>
        </div>
      </div>
    </div>
    <div class="chat-input">
      <input
        v-model="userInput"
        @keyup.enter="sendMessage"
        placeholder="输入消息..."
        type="text"
        :disabled="loading"
      />
      <button @click="sendMessage" :disabled="loading">
        <span v-if="!loading">发送</span>
        <span v-else>...</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.ai-chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
  max-width: 540px;
  border-radius: 18px;
  overflow: hidden;
  margin: 0 auto;
  background: linear-gradient(135deg, #e0e7ff 0%, #f8fafc 100%);
  box-shadow: 0 6px 32px rgba(80, 120, 200, 0.12), 0 1.5px 6px rgba(0,0,0,0.04);
  border: none;
  position: relative;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 32px 24px 18px 12px;
  background: transparent;
  display: flex;
  flex-direction: column;
  gap: 0;
  scroll-behavior: smooth;
  text-align: left;
}

.message {
  display: flex;
  align-items: flex-start; /* 顶部对齐 */
  margin-bottom: 18px;
  min-height: 36px;
}

.user-message {
  flex-direction: row-reverse;
  justify-content: flex-end;
  align-items: flex-start; /* 顶部对齐 */
}

.ai-message {
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start; /* 顶部对齐 */
}

/* 修复 avatar 拉伸问题，强制 avatar 尺寸不变 */
.avatar {
  flex: 0 0 auto;
  width: 38px;
  height: 38px;
  min-width: 38px;
  min-height: 38px;
  max-width: 38px;
  max-height: 38px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.45rem;
  margin: 0 8px;
  box-shadow: 0 2px 8px rgba(99,102,241,0.10);
  color: #fff;
  user-select: none;
  /* 防止子元素撑开 */
  overflow: hidden;
}

.user-message .avatar {
  background: linear-gradient(135deg, #f59e42 0%, #fbbf24 100%);
  color: #fff;
}

.message-content {
  max-width: 70vw;
  min-width: 1.5;
  padding: 14px 20px;
  border-radius: 6px 18px 18px 18px;
  font-size: 1.08rem;
  line-height: 1.5;
  box-shadow: 0 2px 8px rgba(99,102,241,0.06);
  background: #fff;
  color: #333;
  word-break: break-word;
  position: relative;
  transition: background 0.2s;
  animation: fadeInBubble 0.5s;
}

.user-message .message-content {
  background: linear-gradient(90deg, #6366f1 0%, #3b82f6 100%);
  color: #fff;
  border-radius: 6px 18px 18px 18px;
  box-shadow: 0 2px 8px rgba(245,158,66,0.08);
  margin-right: 0; /* 保证右侧紧贴avatar */
  margin-left: 0;
}

.ai-message .message-content {
  background: #f3f4f6;
  color: #333;
  border-radius: 6px 18px 18px 18px;
  margin-left: 0;
  margin-right: 0;
}

.message-content.loading {
  display: flex;
  align-items: center;
  font-style: italic;
  color: #6366f1;
  background: #eef2ff;
}

.dot {
  display: inline-block;
  width: 7px;
  height: 7px;
  margin-right: 3px;
  border-radius: 50%;
  background: #6366f1;
  animation: blink 1.2s infinite both;
}
.dot:nth-child(1) { animation-delay: 0s; }
.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes blink {
  0%, 80%, 100% { opacity: 0.2; }
  40% { opacity: 1; }
}

@keyframes fadeInBubble {
  from { opacity: 0; transform: translateY(20px);}
  to { opacity: 1; transform: translateY(0);}
}

.chat-input {
  display: flex;
  padding: 18px 24px 18px 24px;
  background: #fff;
  border-top: 1.5px solid #e0e7ef;
  align-items: center;
  gap: 12px;
}

.chat-input input {
  flex: 1;
  padding: 12px 18px;
  border: 1.5px solid #c7d2fe;
  border-radius: 22px;
  font-size: 1.08rem;
  outline: none;
  background: #f8fafc;
  transition: border 0.2s;
  box-shadow: 0 1px 4px rgba(99,102,241,0.04);
}
.chat-input input:focus {
  border: 1.5px solid #6366f1;
  background: #fff;
}

.chat-input input:disabled {
  background: #f3f4f6;
  color: #aaa;
}

.chat-input button {
  padding: 10px 28px;
  background: linear-gradient(90deg, #6366f1 0%, #3b82f6 100%);
  color: #fff;
  border: none;
  border-radius: 22px;
  font-size: 1.08rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(99,102,241,0.10);
  transition: background 0.2s, transform 0.1s;
  letter-spacing: 1px;
}
.chat-input button:disabled {
  background: #c7d2fe;
  color: #fff;
  cursor: not-allowed;
}
.chat-input button:hover:not(:disabled) {
  background: linear-gradient(90deg, #3b82f6 0%, #6366f1 100%);
  transform: translateY(-2px) scale(1.03);
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

.bubble-enter-active, .bubble-leave-active {
  transition: all 0.4s cubic-bezier(.55,0,.1,1);
}
.bubble-enter-from {
  opacity: 0;
  transform: translateY(30px) scale(0.95);
}
.bubble-leave-to {
  opacity: 0;
  transform: translateY(-30px) scale(0.95);
}
.AI-img {
  width: 28px; 
  height: 28px; 
  vertical-align: middle;
}
</style>


<script>
export default {
  name: 'AIChat',
  data() {
    return {
      userInput: '',
      messages: [],
      loading: true, //初始化为true，直到ai先说话
      chat_id: '',
      socket: null,
      connected: false,
      errorMessage: '',
      chatComplete: false,
      endFlag: false,
    }
  },
  created (){
    console.log('created')
  },
  mounted () {
    console.log("onMounted")
    this.$ws.addMessageListener(this.handleMessage);
    this.$ws.send(JSON.stringify({ 
      type: 'create', 
      sample_name: this.$store.state.userInfo.userName || 'noname', 
      sample_id: this.$store.state.userInfo.userId || 'noid'
    }));
  },
  unmounted (){
    this.$ws.removeMessageListener(this.handleMessage);
  },
  methods: {
    sendMessage() {
      // console.log(this.loading);
      if (!this.userInput.trim() || this.loading) return;
      
      // Add user message
      this.messages.push({
        content: this.userInput,
        isUser: true
      });
      
      const userMessage = this.userInput;
      this.userInput = '';
      this.loading = true;
      
      this.$ws.send(JSON.stringify({
        type: 'chat',
        chat_id: this.chat_id,
        content: userMessage
      }));
    },
    handleMessage (data) {
      const response = JSON.parse(data);
      console.log('收到服务器消息:', response);
      
      switch (response.type) {
        case 'created':
          this.chat_id = response.chat_id;
          break;
        case 'chat':
          if (response.content) {
            this.messages.push({
              content: response.content,
              isUser: false
            });
            this.$nextTick(() => {
              window.scrollTo({ top: 0, behavior: "smooth" });
            });
          }
          this.loading = false;

          // 检查是否是聊天结束
          if (response.content && response.content.includes('聊天已结束')) {
            this.$store.commit('setStateToNext', { currentState: this.$store.state.flowState, delay: 2000 });
            this.endFlag = true;
          }
      }
    },
    showError(msg) {
      this.errorMessage = msg;
    }
  },
}
</script>