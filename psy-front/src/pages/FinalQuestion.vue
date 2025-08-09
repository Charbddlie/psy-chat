<template>
  <div class="q-bg">
    <!-- 会话选择弹窗 -->
    <transition name="fade">
      <div v-if="showSessionModal" class="session-modal">
        <div class="session-modal-content">
          <span class="session-modal-close" @click="cancelSessionSelection">&times;</span>
          <div class="session-modal-header">
            <h3>检测到历史记录</h3>
            <p>发现您超过7天的实验记录，请选择:</p>
          </div>
          <div class="session-modal-body">
            <div v-if="loadingSessions" class="session-loading">
              <div class="dot"></div>
              <div class="dot"></div>
              <div class="dot"></div>
              <span>加载中...</span>
            </div>
            <div v-else>
              <div v-for="(session, index) in sessions" :key="index" class="session-item" @click="selectSession(session)">
                <div class="session-info">
                  <div class="session-name">用户: {{session.user_name}}</div>
                  <div class="session-progress">
                    <span v-if="session.info" class="progress-item completed">基本信息已收集</span>
                    <span v-else class="progress-item">基本信息未收集</span>
                    <!-- <span v-if="session.pre" :class="['progress-item', session.excluded ? 'excluded' : 'completed']">
                      {{ session.excluded ? '前测不合要求' : '前测已完成' }}
                    </span> -->
                    <!-- 暂时先不显示是否已排除 -->
                    <span v-if="session.pre" :class="['progress-item', 'completed']">
                      前测已完成
                    </span>
                    <span v-else class="progress-item">前测未完成</span>
                    <span v-if="session.chat" class="progress-item completed">AI对话 {{ session.chat_complete ? '(已完成)' : '(未完成)' }}</span>
                    <span v-else class="progress-item">AI对话未开始</span>
                    <span v-if="session.post" class="progress-item completed">后测已完成</span>
                    <span v-else class="progress-item">后测未完成</span>
                    <span v-if="session.timestamp" class="progress-item completed">{{ session.timestamp }}</span>
                    <span v-else class="progress-item">时间未知</span>
                  </div>
                </div>
                <div class="session-action">
                  <span class="select-button">选择</span>
                </div>
              </div>
            </div>
          </div>
          <div class="session-modal-footer">
            <button class="create-new-btn" @click="cancelSessionSelection">创建新会话</button>
          </div>
        </div>
      </div>
    </transition>
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
    <!-- 用户名输入表单 -->
    <div v-if="step === 1" class="q-card">
      <h2 class="q-title">📝 用户验证</h2>
      <div class="q-content">
        <form @submit.prevent="handleNameSubmit" class="q-form">
          <div class="q-question-block">
            <div class="q-question">
              <span class="q-qindex">1.</span>
              如何称呼您？
            </div>
            <input type="text" v-model="form.user_name" class="q-input-short" placeholder="请填写" />
            <br><span v-if="!form.user_name && form_uncomplete" class="q-error-tip">请填写昵称</span>
          </div>
          <button type="submit" class="q-submit-btn">提交</button>
        </form>
      </div>
    </div>
    <!-- 闪电知识后测 -->
    <div v-if="step === 2" class="q-card">
      <h2 class="q-title">⚡ 闪电形成知识后测</h2>
      <div class="q-content">
        <div class="q-instruction">
          请根据您目前的了解回答以下问题。这不是考试，如不确定可选择“不记得了”。
        </div>
        <SelectQuestion :questions="knowledgeQuestions" v-model="knowledgeAnswers"/>
        <button class="q-submit-btn" @click="handleKnowledgeSubmit">提交</button>
      </div>
    </div>
    <!-- 占位部分 -->
    <div v-if="step === 3" class="q-card">
      <div class="q-question-block" style="text-align:center;">
        <div style="color:#22c55e;font-weight:600;">
          后测已完成！感谢您的参与
          <span style="font-size:0.98em;"></span>
        </div>
        <!-- <div v-if="comebackInfo" style="color:#ef4444;font-weight:600;">
          {{ comebackInfo }}<br>
          <span style="font-size:0.98em;">感谢您的配合！</span>
        </div>
        <div v-else style="color:#22c55e;font-weight:600;">
          后测已完成！感谢您的参与
          <span style="font-size:0.98em;"></span>
        </div> -->
      </div>
    </div>
  </div>
</template>

<script>
import SelectQuestion from './components/SelectQuestion.vue';
import { checkFill } from '@/tools';

export default {
  name: 'FinalQuestionnaire',
  components: { SelectQuestion },
  data() {
    return {
      step: 1,
      form: {
        user_name: '',
        time: '',
      },
      form_uncomplete: false,
      errorMessage: '',
      showSessionModal: false,
      sessions: [],
      comebackInfo: null,
      loadingSessions: false,
      knowledgeQuestions: [
        {
          text: '闪电形成的第一步是什么？',
          options: [
            { value: 'A', text: '冰晶碰撞' },
            { value: 'B', text: '冷暖空气相遇' },
            { value: 'C', text: '云层形成' },
            { value: 'D', text: '不记得了' },
          ],
        },
        {
          text: '暖空气为什么会上升？',
          options: [
            { value: 'A', text: '风力推动' },
            { value: 'B', text: '密度变小产生浮力' },
            { value: 'C', text: '压力变化' },
            { value: 'D', text: '不记得了' },
          ],
        },
        {
          text: '云中电荷是如何产生的？',
          options: [
            { value: 'A', text: '冰晶碰撞摩擦' },
            { value: 'B', text: '温度变化' },
            { value: 'C', text: '磁场作用' },
            { value: 'D', text: '不记得了' },
          ],
        },
        {
          text: '云层的电荷分布特点是什么？',
          options: [
            { value: 'A', text: '上正下负' },
            { value: 'B', text: '上负下正' },
            { value: 'C', text: '均匀分布' },
            { value: 'D', text: '不记得了' },
          ],
        },
        {
          text: '闪电放电的本质是什么？',
          options: [
            { value: 'A', text: '电荷中和' },
            { value: 'B', text: '空气燃烧' },
            { value: 'C', text: '磁场变化' },
            { value: 'D', text: '不记得了' },
          ],
        },
      ],
      knowledgeAnswers: Array(5).fill(''),
      submitting: false,
    };
  },
  created() {
    this.$cookies.set('flowState', 'finalTest');
    this.$nextTick(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  },
  methods: {
    handleNameSubmit() {
      this.form_uncomplete = false;
      if (!this.form.user_name || this.form.user_name.trim() === '') {
        this.form_uncomplete = true;
        this.showError('请填写昵称');
        return;
      }
      // 设置时间戳
      const now = new Date();
      const pad = n => n.toString().padStart(2, '0');
      this.form.time =
        now.getFullYear() + '-' +
        pad(now.getMonth() + 1) + '-' +
        pad(now.getDate()) + ' ' +
        pad(now.getHours()) + ':' +
        pad(now.getMinutes()) + ':' +
        pad(now.getSeconds());
      // 更新store中的user_name
      // this.$store.commit('setUserInfo', { user_name: this.form.user_name });
      // 查询会话
      this.$ws.addMessageListener(this.handleSessionQueryMessage);
      this.loadingSessions = true;
      this.$ws.send(JSON.stringify({
        type: 'session_query',
        search_name: this.form.user_name,
      }));
    },
    handleSessionQueryMessage(response) {
      if (response.type === 'query_result') {
        this.$ws.removeMessageListener(this.handleSessionQueryMessage);
        this.loadingSessions = false;
        if (!response.records || response.records.length === 0) {
          this.errorMessage = '抱歉，未找到用户记录，请检查名称';
          return;
        }
        // 先过滤掉 info/pre/post/chat_complete 不是全部为 true 的记录
        response.records = (response.records || []).filter(record => {
          return record.info === true && record.pre === true && record.post === true && record.chat_complete === true;
        });
        if (!response.records || response.records.length === 0) {
          this.errorMessage = '抱歉，有用户记录但是没有找到已完成的答题记录';
          return;
        }
        console.log(response.records)
        // 只需要天数大于7天即可，比如3号的记录需要10号
        const today = new Date();
        response.records = (response.records || []).filter(record => {
          if (!record.timestamp) return false;
          const recordDate = new Date(Number(record.timestamp) * 1000);
          // 只比较日期，不考虑具体时间
          const diffTime = today.setHours(0,0,0,0) - recordDate.setHours(0,0,0,0);
          const diffDays = diffTime / (1000 * 60 * 60 * 24);
          return diffDays > 7;
        });
        console.log(response.records)
        if (!response.records || response.records.length === 0) {
          this.errorMessage = '抱歉，离上次答题还不满7天';
          return;
        }
        // 格式化时间戳
        this.sessions = response.records.map(record => {
          if (record.timestamp) {
            const ts = Number(record.timestamp) * 1000;
            const date = new Date(ts);
            const pad = n => n.toString().padStart(2, '0');
            record.timestamp =
              date.getFullYear() +
              pad(date.getMonth() + 1) +
              pad(date.getDate()) + ' ' +
              pad(date.getHours()) + ':' +
              pad(date.getMinutes());
          } else {
            record.timestamp = '';
          }
          return record;
        });
        console.log(this.sessions)
        if (this.sessions.length > 0) {
          this.showSessionModal = true;
        } else {
          this.errorMessage = '抱歉，出现了未知错误';
        }
      }
    },
    selectSession(session) {
      this.showSessionModal = false;
      this.$ws.send(JSON.stringify({
        type: 'chat_create',
        user_name: session.user_name,
        user_id: session.user_id,
      }));
      const checkChatIdInterval = setInterval(() => {
        if (this.$store.state.userInfo.user_id && this.$store.state.userInfo.user_id !== '') {
          clearInterval(checkChatIdInterval);
          this.step = 2; // 进入问卷步骤
        }
      }, 100);
    },
    cancelSessionSelection() {
      this.showSessionModal = false;
      // 占位：在这里添加其他代码
      this.step = 3;
    },
    handleKnowledgeSubmit() {
      if (!checkFill(this, this.knowledgeAnswers)) return;
      if (this.submitting) return;
      this.submitting = true;
      // 计算分数
      const correctAnswers = ['B', 'B', 'A', 'A', 'A'];
      const score = this.knowledgeAnswers.reduce((sum, answer, index) => sum + (answer === correctAnswers[index] ? 1 : 0), 0);
      // 组装payload
      const payload = {
        user_id: this.$store.state.userInfo.user_id,
        user_name: this.$store.state.userInfo.user_name,
        time: this.form.time,
        knowledgePayload: {
          questions: this.knowledgeQuestions,
          answers: this.knowledgeAnswers.slice(),
          score: score,
        },
      }
      // 提交到后端
      this.$ws.send(JSON.stringify({
        type: 'final_questionnaire',
        data: payload,
        user_id: this.$store.state.userInfo.user_id,
      }));
      this.step = 3;
      this.submitting = false;
    },
    showError(msg) {
      this.errorMessage = msg;
    },
  },
};
</script>

<style scoped>
/* 复用 InfoCollect 的样式 */
.session-modal {
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.session-modal-content {
  background-color: #fff;
  margin: auto;
  padding: 20px;
  width: 90%;
  max-width: 500px;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  position: relative;
}
.session-modal-close {
  position: absolute;
  top: 10px;
  right: 15px;
  color: #666;
  font-size: 24px;
  cursor: pointer;
}
.session-modal-header {
  margin-bottom: 15px;
  text-align: center;
}
.session-modal-header h3 {
  font-size: 22px;
  color: #333;
  margin-bottom: 10px;
}
.session-modal-header p {
  color: #666;
  margin: 5px 0;
}
.session-modal-body {
  max-height: 300px;
  overflow-y: auto;
}
.session-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.session-item:hover {
  border-color: #6366f1;
  background-color: #f8fafc;
  transform: translateY(-2px);
}
.session-info {
  flex: 1;
}
.session-name {
  font-weight: bold;
  margin-bottom: 5px;
}
.session-progress {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 5px;
}
.progress-item {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 12px;
  background: #f3f4f6;
  color: #666;
}
.progress-item.completed {
  background: #dbeafe;
  color: #2563eb;
}
.progress-item.excluded {
  background: #dbeafe;
  color: #e53935;
}
.session-action {
  margin-left: 15px;
}
.select-button {
  display: inline-block;
  padding: 5px 15px;
  background: linear-gradient(90deg, #6366f1 0%, #3b82f6 100%);
  color: white;
  border-radius: 15px;
  font-size: 14px;
  transition: all 0.2s;
}
.select-button:hover {
  transform: scale(1.05);
}
.session-modal-footer {
  text-align: center;
  margin-top: 15px;
}
.create-new-btn {
  padding: 8px 20px;
  background: #f3f4f6;
  border: none;
  border-radius: 20px;
  color: #333;
  cursor: pointer;
  transition: all 0.2s;
}
.create-new-btn:hover {
  background: #e5e7eb;
}
.session-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.session-loading .dot {
  width: 8px;
  height: 8px;
  margin: 0 4px;
  border-radius: 50%;
  background: #6366f1;
  animation: pulse 1.5s infinite ease-in-out;
}
.session-loading .dot:nth-child(2) {
  animation-delay: 0.3s;
}
.session-loading .dot:nth-child(3) {
  animation-delay: 0.6s;
}
.session-loading span {
  margin-left: 10px;
  color: #666;
}
@keyframes pulse {
  0%, 100% { transform: scale(0.5); opacity: 0.3; }
  50% { transform: scale(1); opacity: 1; }
}
.error-modal {
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.error-modal-content {
  background-color: #fff;
  margin: auto;
  padding: 20px;
  width: 80%;
  max-width: 400px;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  position: relative;
  text-align: center;
}
.error-modal-close {
  position: absolute;
  top: 10px;
  right: 15px;
  color: #666;
  font-size: 24px;
  cursor: pointer;
}
.error-modal-icon {
  font-size: 36px;
  margin-bottom: 15px;
}
.error-modal-text {
  font-size: 18px;
  color: #333;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>