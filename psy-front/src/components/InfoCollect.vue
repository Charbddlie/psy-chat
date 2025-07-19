<template>
  <div class="q-bg">
    <div class="q-card">
      <h2 class="q-title">📝 基本信息问卷</h2>
      <div class="q-content">
        <form @submit.prevent="handleSubmit" class="q-form">
          <div class="q-question-block">
            <div class="q-question">
              <span class="q-qindex">1.</span>
              姓名
            </div>
            <input type="text" v-model="form.name" class="q-input-short" placeholder="请填写" />
            <br><span v-if="!form.name && form_uncomplete" class="q-error-tip">请填写姓名</span>
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
              <label class="q-option" :class="{ selected: form.gender === '其他' }">
                <input type="radio" class="q-radio" value="其他" v-model="form.gender" /> 其他
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
          <div class="q-question-block">
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
          </div>
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
import '@/assets/questionnaire.css'
import config from '@/config.js'
export default {
  name: 'InfoCollect',
  data() {
    return {
      form: {
        id: '',
        name: '',
        age: '',
        gender: '',
        major: '',
        majorOther: '',
        grade: '',
        aiFrequency: '',
        aiAttitude: '',
        time: '',
      },
      submitted: false,
      form_uncomplete: false,
    }
  },
  created() {
    // 生成8位随机id
    const randomId = Math.random().toString(36).substring(2, 10);
    this.form.id = randomId;
    this.$store.commit('setUserInfo', { id: randomId });
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
      this.$store.commit('setUserInfo', { name: this.form.name });
      // 处理“其他”专业
      let major = this.form.major;
      if (major === '其他' && this.form.majorOther.trim()) {
        major = this.form.majorOther.trim();
      }
      // 检查除了majorOther之外form的所有字段是否都有值
      const requiredFields = ['name', 'age', 'gender', 'major', 'grade', 'aiFrequency', 'aiAttitude'];
      for (const field of requiredFields) {
        if (!this.form[field] || (typeof this.form[field] === 'string' && this.form[field].trim() === '')) {
          this.form_uncomplete = true;
          return;
        }
      }

      // 将表单数据组装成 JSON
      const payload = {
        ...this.form,
        major
      };
      // 发送 POST 请求到本地 8764 端口
      fetch(`${config.apiBaseUrl}/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })
      .then(response => {
        if (response.ok) {
          console.log('提交结果:', response);
          this.submitted = true;
          this.$store.commit('setStateToNext', { currentState: this.$store.state.flowState, delay: 0 });
        } else {
          // 可以根据需要处理错误
          console.error('提交失败: 服务器返回错误');
        }
      })
      .catch(err => {
        // 可以根据需要处理错误
        console.error('提交失败:', err);
      });
    }
  }
}
</script>