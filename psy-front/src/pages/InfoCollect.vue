<template>
  <div class="q-bg">
    <!-- 会话选择弹窗 -->
    <transition name="fade">
      <div v-if="showSessionModal" class="session-modal">
        <div class="session-modal-content">
          <span class="session-modal-close" @click="cancelSessionSelection">&times;</span>
          <div class="session-modal-header">
            <h3>检测到历史记录</h3>
            <p>发现您之前的实验记录，请选择:</p>
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
                    
                    <span v-if="session.pre" :class="['progress-item', session.excluded ? 'excluded' : 'completed']">
                      {{ session.excluded ? '前测不合要求' : '前测已完成' }}
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
    <div class="q-card">
      <h2 class="q-title">📝 基本信息问卷</h2>
      <div class="q-content">
        <form @submit.prevent="handleSubmit" class="q-form">
          <div class="q-question-block">
            <div class="q-question">
              <span class="q-qindex">1.</span>
              如何称呼您？
            </div>
            <input type="text" v-model="form.user_name" class="q-input-short" placeholder="请填写" />
            <br><span v-if="!form.user_name && form_uncomplete" class="q-error-tip">请填写昵称</span>
          </div>
          <div class="q-question-block">
            <div class="q-question">
              <span class="q-qindex">2.</span>
              年龄
            </div>
            <input type="number" v-model="form.age" class="q-input-short" min="0" max="120" placeholder="请填写" />
            <span class="q-unit">岁</span>
            <br><span v-if="(!form.age || form.age < 0 || form.age > 120) && form_uncomplete" class="q-error-tip">请填写有效年龄</span>
          </div>
          <div class="q-question-block">
            <div class="q-question">
              <span class="q-qindex">3.</span>
              性别
            </div>
            <div class="q-options">
              <label class="q-option" :class="{ selected: form.gender === '男' }">
                <input type="radio" class="q-radio" value="男" v-model="form.gender" /> 男
              </label>
              <label class="q-option" :class="{ selected: form.gender === '女' }">
                <input type="radio" class="q-radio" value="女" v-model="form.gender" /> 女
              </label>
            </div>
            <br><span v-if="!form.gender && form_uncomplete" class="q-error-tip">请选择性别</span>
          </div>
          <div class="q-question-block">
            <div class="q-question">
              <span class="q-qindex">4.</span>
              专业类别
            </div>
            <div class="q-options q-options-vertical">
              <label class="q-option" :class="{ selected: form.major === '理工科' }"><input type="radio" class="q-radio" value="理工科" v-model="form.major" /> 理工科（物理、化学、工程、数学、计算机等）</label>
              <label class="q-option" :class="{ selected: form.major === '文科' }"><input type="radio" class="q-radio" value="文科" v-model="form.major" /> 文科（中文、历史、哲学、教育学等）</label>
              <label class="q-option" :class="{ selected: form.major === '社科' }"><input type="radio" class="q-radio" value="社科" v-model="form.major" /> 社科（心理学、社会学、政治学等）</label>
              <label class="q-option" :class="{ selected: form.major === '其他' }">
                <input type="radio" class="q-radio" value="其他" v-model="form.major" />
                其他：
                <input type="text" v-model="form.majorOther" :disabled="form.major !== '其他'" class="q-input-long" placeholder="请填写" />
              </label>
            </div>
            <br><span v-if="!form.major && form_uncomplete" class="q-error-tip">请选择专业类别</span>
          </div>
          <div class="q-question-block">
            <div class="q-question">
              <span class="q-qindex">5.</span>
              年级
            </div>
            <div class="q-options">
              <label class="q-option" :class="{ selected: form.grade === '大一' }"><input type="radio" class="q-radio" value="大一" v-model="form.grade" /> 大一</label>
              <label class="q-option" :class="{ selected: form.grade === '大二' }"><input type="radio" class="q-radio" value="大二" v-model="form.grade" /> 大二</label>
              <label class="q-option" :class="{ selected: form.grade === '大三' }"><input type="radio" class="q-radio" value="大三" v-model="form.grade" /> 大三</label>
              <label class="q-option" :class="{ selected: form.grade === '大四' }"><input type="radio" class="q-radio" value="大四" v-model="form.grade" /> 大四</label>
              <label class="q-option" :class="{ selected: form.grade === '研究生' }"><input type="radio" class="q-radio" value="研究生" v-model="form.grade" /> 研究生</label>
            </div>
            <br><span v-if="!form.grade && form_uncomplete" class="q-error-tip">请选择年级</span>
          </div>
          <!-- <div class="q-question-block">
            <div class="q-question">
              <span class="q-qindex">6.</span>
              您使用AI助手（如ChatGPT、文心一言、小爱同学等）的频率
            </div>
            <div class="q-options">
              <label class="q-option" :class="{ selected: form.aiFrequency === '从不' }"><input type="radio" class="q-radio" value="从不" v-model="form.aiFrequency" /> 从不</label>
              <label class="q-option" :class="{ selected: form.aiFrequency === '很少' }"><input type="radio" class="q-radio" value="很少" v-model="form.aiFrequency" /> 很少</label>
              <label class="q-option" :class="{ selected: form.aiFrequency === '有时' }"><input type="radio" class="q-radio" value="有时" v-model="form.aiFrequency" /> 有时</label>
              <label class="q-option" :class="{ selected: form.aiFrequency === '经常' }"><input type="radio" class="q-radio" value="经常" v-model="form.aiFrequency" /> 经常</label>
              <label class="q-option" :class="{ selected: form.aiFrequency === '总是' }"><input type="radio" class="q-radio" value="总是" v-model="form.aiFrequency" /> 总是</label>
            </div>
            <br><span v-if="!form.aiFrequency && form_uncomplete" class="q-error-tip">请选择频率</span>
          </div> -->
          <div class="q-question-block">
            <div class="q-question">
              <span class="q-qindex">7.</span>
              您对AI技术的总体态度
            </div>
            <div class="q-options q-options-vertical">
              <label class="q-option" :class="{ selected: form.aiAttitude === '非常消极' }"><input type="radio" class="q-radio" value="非常消极" v-model="form.aiAttitude" /> 非常消极</label>
              <label class="q-option" :class="{ selected: form.aiAttitude === '比较消极' }"><input type="radio" class="q-radio" value="比较消极" v-model="form.aiAttitude" /> 比较消极</label>
              <label class="q-option" :class="{ selected: form.aiAttitude === '中性' }"><input type="radio" class="q-radio" value="中性" v-model="form.aiAttitude" /> 中性</label>
              <label class="q-option" :class="{ selected: form.aiAttitude === '比较积极' }"><input type="radio" class="q-radio" value="比较积极" v-model="form.aiAttitude" /> 比较积极</label>
              <label class="q-option" :class="{ selected: form.aiAttitude === '非常积极' }"><input type="radio" class="q-radio" value="非常积极" v-model="form.aiAttitude" /> 非常积极</label>
            </div>
            <br><span v-if="!form.aiAttitude && form_uncomplete" class="q-error-tip">请选择态度</span>
          </div>
          <button type="submit" class="q-submit-btn">提交</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
// import { inject } from 'vue';
export default {
  name: 'InfoCollect',
  data() {
    return {
      form: {
        user_name: '',
        age: '',
        gender: '',
        major: '',
        majorOther: '',
        grade: '',
        // aiFrequency: '',
        aiAttitude: '',
        time: '',
      },
      submitted: false,
      form_uncomplete: false,
      errorMessage: '',
      // 选择user
      showSessionModal: false,
      sessions: [],
      loadingSessions: false,
    }
  },
  created() {
    this.$cookies.set('flowState', 'collectInfo');
    this.$nextTick(() => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  },
  watch: {
    'form.major'(val) {
      if (val !== '其他') {
        this.form.majorOther = '';
      }
    }
  },
  methods: {
    handleSubmit() {
      this.form_uncomplete = false;

      // 设置form.time为心理学研究处理时间的常用格式（YYYY-MM-DD HH:MM:SS）
      const now = new Date();
      const pad = n => n.toString().padStart(2, '0');
      this.form.time = 
        now.getFullYear() + '-' +
        pad(now.getMonth() + 1) + '-' +
        pad(now.getDate()) + ' ' +
        pad(now.getHours()) + ':' +
        pad(now.getMinutes()) + ':' +
        pad(now.getSeconds());
      // 更新store中的id
      this.$store.commit('setUserInfo', { user_name: this.form.user_name });
      // 处理“其他”专业
      let major = this.form.major;
      if (major === '其他' && this.form.majorOther.trim()) {
        major = this.form.majorOther.trim();
      }
      // 检查除了majorOther之外form的所有字段是否都有值
      // const requiredFields = ['user_name', 'age', 'gender', 'major', 'grade', 'aiFrequency', 'aiAttitude'];
      const requiredFields = ['user_name', 'age', 'gender', 'major', 'grade', 'aiAttitude'];
      for (const field of requiredFields) {
        if (!this.form[field] || (typeof this.form[field] === 'string' && this.form[field].trim() === '')) {
          this.form_uncomplete = true;
          this.showError("填写未完成")
          return;
        }
      }

      // 将表单数据组装成 JSON
      this.payload = {
        ...this.form,
        major
      };

      if (this.$store.state.chat_id){
        this.submitInfo(); 
      }
      else{
        // 如果chat_id未设置，就证明没有创建，需要user query，再创建
        // 先提交info会导致创建记录，从而导致查询到正在进行的session
        this.$ws.addMessageListener(this.handleSessionQueryMessage);
        this.loadingSessions = true;
        this.$ws.send(JSON.stringify({
          type: "session_query",
          search_name: this.form.user_name,
        }))
      }
    },
    showError(msg) {
      this.errorMessage = msg;
    },
    handleSessionQueryMessage(response) {
      if (response.type == "query_result") {
        this.$ws.removeMessageListener(this.handleSessionQueryMessage);
        this.loadingSessions = false;
          
        // 检查是否有匹配的会话
        if (response.records && response.records.length > 0) {
          console.log(response.records)
          // 显示会话选择模态框
          this.sessions = response.records.map(record => {
            if (record.timestamp) {
              const ts = Number(record.timestamp) * 1000;
              const date = new Date(ts);
              const pad = n => n.toString().padStart(2, '0');
              record.timestamp = 
                date.getFullYear().toString() +
                pad(date.getMonth() + 1) +
                pad(date.getDate()) + ' ' +
                pad(date.getHours()) + ':' +
                pad(date.getMinutes())
            } else {
              record.timestamp = '';
            }
            return record;
          });
          console.log(this.sessions)
          this.showSessionModal = true;
        } else {
          // 没有匹配记录，直接创建新会话
          this.createNewSession();
        }
      }
    },
    // 创建新会话
    createNewSession() {
      this.$ws.send(JSON.stringify({
        type: 'chat_create',
        user_name: this.form.user_name,
      }));
      // 每0.5秒检查user_id，直到不为空字符串再调用submitInfo
      const checkChatIdInterval = setInterval(() => {
        if (this.$store.state.userInfo.user_id && this.$store.state.userInfo.user_id !== '') {
          clearInterval(checkChatIdInterval);
          this.submitInfo();
        }
      }, 500);
    },
    // 选择现有会话
    selectSession(session) {
      this.showSessionModal = false;
      this.$ws.send(JSON.stringify({
        type: 'chat_create',
        user_name: session.user_name,
        user_id: session.user_id,
      }));
      // 每0.5秒检查chat_id，直到不为空字符串再调用submitInfo
      const checkChatIdInterval = setInterval(() => {
        if (this.$store.state.userInfo.user_id && this.$store.state.userInfo.user_id !== '') {
          clearInterval(checkChatIdInterval);
          this.submitInfo();
        }
      }, 100);
    },
    // 取消会话选择，开始新会话
    cancelSessionSelection() {
      this.showSessionModal = false;
      this.createNewSession();
    },
    submitInfo() {
      this.$ws.send(JSON.stringify({
        type: 'info_collect',
        data: this.payload,
        user_id: this.$store.state.userInfo.user_id
      }))
      this.$store.commit('setStateToNext', { switchState: this.$store.state.flowStateEnum.collectInfo, delay: 0 });
    }
  }
}
</script>

<style scoped>
/* 会话选择模态框样式 */
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

/* 错误弹窗样式 */
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

/* 淡入淡出动画 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>