<template>
  <div class="info-collect">
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label>1. 姓名<span style="color: red">*:</span></label>
        <input type="text" v-model="form.name" placeholder="请填写"  style="width: 60px;" />
        <span v-if="!form.name && form_uncomplete" style="color: red; font-size: 12px;">请填写姓名</span>
      </div>

      <div class="form-group">
        <label>2. 年龄<span style="color: red">*:</span></label>
        <input type="number" v-model="form.age" placeholder="请填写" min="0" max="120"  style="width: 60px;" /> 岁
        <span v-if="(!form.age || form.age < 0 || form.age > 120) && form_uncomplete" style="color: red; font-size: 12px;">请填写有效年龄</span>
      </div>

      <div class="form-group">
        <label>3. 性别<span style="color: red">*:</span></label>
        <label><input type="radio" value="男" v-model="form.gender"  /> 男</label>
        <label><input type="radio" value="女" v-model="form.gender"  /> 女</label>
        <label><input type="radio" value="其他" v-model="form.gender"  /> 其他</label>
        <span v-if="!form.gender && form_uncomplete" style="color: red; font-size: 12px;">请选择性别</span>
      </div>

      <div class="form-group">
        <label>4. 专业类别<span style="color: red">*:</span></label>
        <br />
        <label><input type="radio" value="理工科" v-model="form.major"  /> 理工科（物理、化学、工程、数学、计算机等）</label>
        <br />
        <label><input type="radio" value="文科" v-model="form.major"  /> 文科（中文、历史、哲学、教育学等）</label>
        <br />
        <label><input type="radio" value="社科" v-model="form.major"  /> 社科（心理学、社会学、政治学等）</label>
        <br />
        <label>
          <input type="radio" value="其他" v-model="form.major"  />
          其他：
          <input type="text" v-model="form.majorOther" :disabled="form.major !== '其他'" placeholder="" style="width: 120px;" />
        </label>
        <span v-if="!form.major && form_uncomplete" style="color: red; font-size: 12px;">请选择专业类别</span>
      </div>

      <div class="form-group">
        <label>5. 年级<span style="color: red">*:</span></label><br />
        <label><input type="radio" value="大一" v-model="form.grade"  /> 大一</label>
        <label><input type="radio" value="大二" v-model="form.grade"  /> 大二</label>
        <label><input type="radio" value="大三" v-model="form.grade"  /> 大三</label>
        <label><input type="radio" value="大四" v-model="form.grade"  /> 大四</label>
        <label><input type="radio" value="研究生" v-model="form.grade"  /> 研究生</label>
        <span v-if="!form.grade && form_uncomplete" style="color: red; font-size: 12px;">请选择年级</span>
      </div>

      <div class="form-group">
        <label>6. 您使用AI助手（如ChatGPT、文心一言、小爱同学等）的频率<span style="color: red">*:</span></label><br />
        <label><input type="radio" value="从不" v-model="form.aiFrequency"  /> 从不</label>
        <label><input type="radio" value="很少" v-model="form.aiFrequency"  /> 很少</label>
        <label><input type="radio" value="有时" v-model="form.aiFrequency"  /> 有时</label>
        <label><input type="radio" value="经常" v-model="form.aiFrequency"  /> 经常</label>
        <label><input type="radio" value="总是" v-model="form.aiFrequency"  /> 总是</label>
        <span v-if="!form.aiFrequency && form_uncomplete" style="color: red; font-size: 12px;">请选择频率</span>
      </div>

      <div class="form-group">
        <label>7. 您对AI技术的总体态度<span style="color: red">*:</span></label><br />
        <label><input type="radio" value="非常消极" v-model="form.aiAttitude"  /> 非常消极</label><br />
        <label><input type="radio" value="比较消极" v-model="form.aiAttitude"  /> 比较消极</label><br />
        <label><input type="radio" value="中性" v-model="form.aiAttitude"  /> 中性</label><br />
        <label><input type="radio" value="比较积极" v-model="form.aiAttitude"  /> 比较积极</label><br />
        <label><input type="radio" value="非常积极" v-model="form.aiAttitude"  /> 非常积极</label>
        <span v-if="!form.aiAttitude && form_uncomplete" style="color: red; font-size: 12px;">请选择态度</span>
      </div>

      <div class="form-group">
        <button type="submit">提交</button>
      </div>
    </form>
    <div v-if="submitted" class="submit-success">
      问卷已提交，谢谢您的参与！
    </div>
  </div>
</template>

<script>
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

      // 生成8位随机id
      const randomId = Math.random().toString(36).slice(2, 10);
      this.form.id = randomId;
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
      this.$store.commit('setUserInfo', { id: randomId });
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
      fetch('http://localhost:8764/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })
      .then(response => {
        if (response.ok) {
          this.submitted = true;
          this.$store.commit('setStateToNext', this.$store.state.flowState);
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
.info-collect {
  max-width: 500px;
  margin: 30px auto;
  padding: 24px 32px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  background: #fafbfc;
  font-size: 16px;
}
.form-group {
  margin-bottom: 18px;
  text-align: left;
}
.form-group label {
  margin-right: 12px;
  font-weight: normal;
}
input[type="number"], input[type="text"] {
  padding: 2px 6px;
  font-size: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button[type="submit"] {
  padding: 6px 18px;
  font-size: 16px;
  background: #409eff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button[type="submit"]:hover {
  background: #3076c9;
}
.submit-success {
  margin-top: 20px;
  color: #2ecc71;
  font-weight: bold;
  text-align: center;
}
</style>
