<template>
  <div class="info-read-container">
    <div class="info-card">
      <h2>🌩️ 欢迎体验 AI 学习助手！</h2>
      <div class="info-content">
        <p>
          <strong>您好！</strong><br>
          接下来您将与一个 <span class="highlight">AI学习助手</span> 进行对话，学习 <span class="topic">“闪电形成”</span> 这个主题。
        </p>
        <ul>
          <li><strong>学习时间：</strong>大约 <span class="highlight">15-20分钟</span></li>
          <li><strong>交流方式：</strong>AI会主动与您对话，您可以自由回应和提问</li>
          <li><strong>学习目标：</strong>理解 <span class="topic">闪电是如何形成的</span></li>
        </ul>
        <p>
          <span class="ai-intro">AI助手会先自我介绍，然后引导您开始学习。您只需要自然地与它对话就可以了！</span>
        </p>
        <div class="start-tip">
          <span>现在我们开始吧！</span>
        </div>
      </div>
      <button class="start-btn" @click="startLearning">进入对话</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InfoRead',
  methods: {
    startLearning() {
      this.$store.commit('setStateToNext', { currentState: this.$store.state.flowState, delay: 0 });
    }
  },
  created() {
    this.$cookies.set('flowState', 'readInfo');
  }
}
</script>

<style scoped>
.info-read-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e0e7ff 0%, #f8fafc 100%);
}
.info-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 6px 32px rgba(80, 120, 200, 0.12), 0 1.5px 6px rgba(0,0,0,0.04);
  padding: 38px 44px 32px 44px;
  max-width: 480px;
  width: 100%;
  text-align: center;
  animation: fadeIn 0.8s;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(30px);}
  to { opacity: 1; transform: translateY(0);}
}
.info-card h2 {
  color: #3b82f6;
  margin-bottom: 18px;
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: 1px;
}
.info-content {
  font-size: 1.13rem;
  color: #333;
  margin-bottom: 24px;
  text-align: left;
}
.info-content ul {
  margin: 12px 0 16px 18px;
  padding: 0;
  list-style: disc;
  color: #444;
}
.info-content li {
  margin-bottom: 6px;
  font-size: 1.05rem;
}
.highlight {
  color: #f59e42;
  font-weight: 600;
}
.topic {
  color: #6366f1;
  font-weight: 600;
  background: #eef2ff;
  border-radius: 4px;
  padding: 0 4px;
}
.ai-intro {
  display: inline-block;
  margin-top: 8px;
  color: #2563eb;
  font-weight: 500;
}
.start-tip {
  margin: 18px 0 0 0;
  font-size: 1.1rem;
  color: #10b981;
  font-weight: 600;
  text-align: center;
  letter-spacing: 1px;
}
.start-btn {
  margin-top: 28px;
  padding: 12px 38px;
  font-size: 1.18rem;
  background: linear-gradient(90deg, #6366f1 0%, #3b82f6 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(99,102,241,0.10);
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
  font-weight: 600;
  letter-spacing: 1px;
}
.start-btn:hover {
  background: linear-gradient(90deg, #3b82f6 0%, #6366f1 100%);
  transform: translateY(-2px) scale(1.03);
}
</style>