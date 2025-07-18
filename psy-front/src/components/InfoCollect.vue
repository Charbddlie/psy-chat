<template>
  <div class="info-collect-bg">
    <div class="info-collect-card">
      <h2 class="collect-title">📝 基本信息问卷</h2>
      <div class="collect-desc">
        <p>
          <span class="highlight">请填写以下信息，所有带 <span style="color: #ef4444">*</span> 的为必填项。</span>
        </p>
      </div>
      <form @submit.prevent="handleSubmit" class="collect-form">
        <div class="form-group">
          <label>1. 姓名<span class="required">*</span></label>
          <input type="text" v-model="form.name" placeholder="请填写" class="input-short" />
          <span v-if="!form.name && form_uncomplete" class="error-tip">请填写姓名</span>
        </div>

        <div class="form-group">
          <label>2. 年龄<span class="required">*</span></label>
          <input type="number" v-model="form.age" placeholder="请填写" min="0" max="120" class="input-short" /> <span class="unit">岁</span>
          <span v-if="(!form.age || form.age < 0 || form.age > 120) && form_uncomplete" class="error-tip">请填写有效年龄</span>
        </div>

        <div class="form-group">
          <label>3. 性别<span class="required">*</span></label>
          <div class="radio-group">
            <label class="radio-label"><input type="radio" value="男" v-model="form.gender" /> 男</label>
            <label class="radio-label"><input type="radio" value="女" v-model="form.gender" /> 女</label>
            <label class="radio-label"><input type="radio" value="其他" v-model="form.gender" /> 其他</label>
          </div>
          <span v-if="!form.gender && form_uncomplete" class="error-tip">请选择性别</span>
        </div>

        <div class="form-group">
          <label>4. 专业类别<span class="required">*</span></label>
          <div class="radio-group vertical">
            <label class="radio-label"><input type="radio" value="理工科" v-model="form.major" /> 理工科（物理、化学、工程、数学、计算机等）</label>
            <label class="radio-label"><input type="radio" value="文科" v-model="form.major" /> 文科（中文、历史、哲学、教育学等）</label>
            <label class="radio-label"><input type="radio" value="社科" v-model="form.major" /> 社科（心理学、社会学、政治学等）</label>
            <label class="radio-label">
              <input type="radio" value="其他" v-model="form.major" />
              其他：
              <input type="text" v-model="form.majorOther" :disabled="form.major !== '其他'" placeholder="请填写" class="input-long" />
            </label>
          </div>
          <span v-if="!form.major && form_uncomplete" class="error-tip">请选择专业类别</span>
        </div>

        <div class="form-group">
          <label>5. 年级<span class="required">*</span></label>
          <div class="radio-group">
            <label class="radio-label"><input type="radio" value="大一" v-model="form.grade" /> 大一</label>
            <label class="radio-label"><input type="radio" value="大二" v-model="form.grade" /> 大二</label>
            <label class="radio-label"><input type="radio" value="大三" v-model="form.grade" /> 大三</label>
            <label class="radio-label"><input type="radio" value="大四" v-model="form.grade" /> 大四</label>
            <label class="radio-label"><input type="radio" value="研究生" v-model="form.grade" /> 研究生</label>
          </div>
          <span v-if="!form.grade && form_uncomplete" class="error-tip">请选择年级</span>
        </div>

        <div class="form-group">
          <label>6. 您使用AI助手（如ChatGPT、文心一言、小爱同学等）的频率<span class="required">*</span></label>
          <div class="radio-group">
            <label class="radio-label"><input type="radio" value="从不" v-model="form.aiFrequency" /> 从不</label>
            <label class="radio-label"><input type="radio" value="很少" v-model="form.aiFrequency" /> 很少</label>
            <label class="radio-label"><input type="radio" value="有时" v-model="form.aiFrequency" /> 有时</label>
            <label class="radio-label"><input type="radio" value="经常" v-model="form.aiFrequency" /> 经常</label>
            <label class="radio-label"><input type="radio" value="总是" v-model="form.aiFrequency" /> 总是</label>
          </div>
          <span v-if="!form.aiFrequency && form_uncomplete" class="error-tip">请选择频率</span>
        </div>

        <div class="form-group">
          <label>7. 您对AI技术的总体态度<span class="required">*</span></label>
          <div class="radio-group vertical">
            <label class="radio-label"><input type="radio" value="非常消极" v-model="form.aiAttitude" /> 非常消极</label>
            <label class="radio-label"><input type="radio" value="比较消极" v-model="form.aiAttitude" /> 比较消极</label>
            <label class="radio-label"><input type="radio" value="中性" v-model="form.aiAttitude" /> 中性</label>
            <label class="radio-label"><input type="radio" value="比较积极" v-model="form.aiAttitude" /> 比较积极</label>
            <label class="radio-label"><input type="radio" value="非常积极" v-model="form.aiAttitude" /> 非常积极</label>
          </div>
          <span v-if="!form.aiAttitude && form_uncomplete" class="error-tip">请选择态度</span>
        </div>

        <div class="form-group center">
          <button type="submit" class="submit-btn">提交</button>
        </div>
      </form>
      <div v-if="submitted" class="submit-success">
        <span>问卷已提交，谢谢您的参与！</span>
      </div>
    </div>
  </div>
</template>

<script>
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
          this.$store.commit('setStateToNext', { currentState: this.$store.state.flowState, delay: 2000 });
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

<style scoped>
.info-collect-bg {
  min-height: 100vh;
  background: linear-gradient(135deg, #e0e7ff 0%, #f8fafc 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}
.info-collect-card {
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
.collect-title {
  color: #3b82f6;
  margin-bottom: 18px;
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: 1px;
}
.collect-desc {
  font-size: 1.08rem;
  color: #444;
  margin-bottom: 18px;
  text-align: left;
}
.highlight {
  color: #f59e42;
  font-weight: 600;
}
.required {
  color: #ef4444;
  margin-left: 2px;
  font-size: 1.1em;
}
.collect-form {
  margin-top: 8px;
  text-align: left;
}
.form-group {
  margin-bottom: 18px;
}
.form-group label {
  font-weight: 500;
  color: #333;
  margin-right: 10px;
}
.input-short {
  width: 80px;
  padding: 4px 8px;
  font-size: 15px;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  margin-left: 6px;
}
.input-long {
  width: 120px;
  padding: 4px 8px;
  font-size: 15px;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  margin-left: 6px;
}
.unit {
  color: #888;
  font-size: 0.98em;
  margin-left: 2px;
}
.radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 16px 18px;
  margin-top: 6px;
  margin-bottom: 2px;
}
.radio-group.vertical {
  flex-direction: column;
  gap: 6px 0;
}
.radio-label {
  font-weight: 400;
  color: #444;
  font-size: 1em;
  display: flex;
  align-items: center;
  gap: 4px;
}
.error-tip {
  display: block;
  color: #ef4444;
  font-size: 12px;
  margin-top: 4px;
  margin-left: 2px;
}
.center {
  text-align: center;
}
.submit-btn {
  margin-top: 10px;
  padding: 10px 38px;
  font-size: 1.13rem;
  background: linear-gradient(90deg, #6366f1 0%, #3b82f6 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(99,102,241,0.10);
  cursor: pointer;
  font-weight: 600;
  letter-spacing: 1px;
  transition: background 0.2s, transform 0.1s;
}
.submit-btn:hover {
  background: linear-gradient(90deg, #3b82f6 0%, #6366f1 100%);
  transform: translateY(-2px) scale(1.03);
}
.submit-success {
  margin-top: 28px;
  color: #10b981;
  font-weight: 600;
  font-size: 1.13rem;
  text-align: center;
  letter-spacing: 1px;
  animation: fadeIn 0.6s;
}
</style>
