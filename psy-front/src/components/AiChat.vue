<template>
  <div class="ai-chat-container">
    <div class="chat-messages" ref="messageContainer">
      <div v-for="(message, index) in messages" :key="index" 
           :class="['message', message.isUser ? 'user-message' : 'ai-message']">
        <div class="message-content">{{ message.content }}</div>
      </div>
    </div>
    <div class="chat-input">
      <input 
        v-model="userInput" 
        @keyup.enter="sendMessage" 
        placeholder="输入消息..." 
        type="text"
      />
      <button @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AiChat',
  data() {
    return {
      userInput: '',
      messages: [],
      loading: false,
      socket: null,
      connected: false
    }
  },
  created() {
    this.connectWebSocket();
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.close();
    }
  },
  methods: {
    connectWebSocket() {
      this.socket = new WebSocket('ws://localhost:8765');
      
      this.socket.onopen = () => {
        console.log('WebSocket连接已建立');
        this.connected = true;
        // 发送start消息启动聊天会话
        this.socket.send(JSON.stringify({ type: 'start' }));
      };
      
      this.socket.onmessage = (event) => {
        const response = JSON.parse(event.data);
        console.log('收到服务器消息:', response);
        this.loading = false
        
        if (response.content) {
          this.messages.push({
            content: response.content,
            isUser: false
          });
          this.scrollToBottom();
        }
      };
      
      this.socket.onerror = (error) => {
        console.error('WebSocket错误:', error);
        this.messages.push({
          content: '连接错误，请检查服务器是否运行',
          isUser: false
        });
      };
      
      this.socket.onclose = () => {
        console.log('WebSocket连接已关闭');
        this.connected = false;
      };
    },
    sendMessage() {
      if (!this.userInput.trim() || this.loading) return;
      
      // Add user message
      this.messages.push({
        content: this.userInput,
        isUser: true
      });
      
      const userMessage = this.userInput;
      this.userInput = '';
      this.loading = true;
      
      // 发送消息到WebSocket服务器
      if (this.connected) {
        this.socket.send(JSON.stringify({
          type: 'chat',
          content: userMessage
        }));
      } else {
        // 如果未连接，尝试重新连接
        this.connectWebSocket();
        setTimeout(() => {
          if (this.connected) {
            this.socket.send(JSON.stringify({
              type: 'chat',
              content: userMessage
            }));
          } else {
            this.messages.push({
              content: '无法连接到服务器',
              isUser: false
            });
            this.loading = false;
          }
        }, 1000);
      }
      
      // 设置超时，如果服务器没有响应
      setTimeout(() => {
        if (this.loading) {
          this.loading = false;
          this.messages.push({
            content: '服务器响应超时',
            isUser: false
          });
          this.scrollToBottom();
        }
      }, 10000);
    },
    scrollToBottom() {
      this.$nextTick(() => {
        if (this.$refs.messageContainer) {
          this.$refs.messageContainer.scrollTop = this.$refs.messageContainer.scrollHeight;
        }
      });
    }
  },
}
</script>

<style scoped>
.ai-chat-container {
  display: flex;
  flex-direction: column;
  height: 500px;
  width: 50%;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  margin: 0 auto; /* 居中显示 */
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background-color: #f9f9f9;
  display: flex;
  flex-direction: column;
}

.message {
  margin-bottom: 12px;
  max-width: 80%;
  display: flex;
}

.user-message {
  justify-content: flex-end; /* 用户消息靠右 */
  align-self: flex-end;
}

.ai-message {
  justify-content: flex-start; /* AI消息靠左 */
  align-self: flex-start;
}

.message-content {
  padding: 10px 14px;
  border-radius: 18px;
  display: inline-block;
  text-align: left;
}

.user-message .message-content {
  background-color: #1e88e5;
  color: white;
}

.ai-message .message-content {
  background-color: #e9e9eb;
  color: #333;
}

.chat-input {
  display: flex;
  padding: 10px;
  background-color: white;
  border-top: 1px solid #ddd;
}

.chat-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 20px;
  margin-right: 8px;
  outline: none;
}

button {
  padding: 10px 20px;
  background-color: #1e88e5;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
}

button:hover {
  background-color: #1976d2;
}
</style>