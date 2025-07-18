<template>
  <div class="info-collect">
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label>1. 姓名：</label>
        <input type="text" v-model="form.name" placeholder="请填写" required style="width: 60px;" />
      </div>

      <div class="form-group">
        <label>2. 年龄：</label>
        <input type="number" v-model="form.age" placeholder="请填写" min="0" max="120" required style="width: 60px;" /> 岁
      </div>

      <div class="form-group">
        <label>3. 性别：</label>
        <label><input type="radio" value="男" v-model="form.gender" required /> 男</label>
        <label><input type="radio" value="女" v-model="form.gender" /> 女</label>
        <label><input type="radio" value="其他" v-model="form.gender" /> 其他</label>
      </div>

      <div class="form-group">
        <label>4. 专业类别：</label>
        <br />
        <label><input type="radio" value="理工科" v-model="form.major" required /> 理工科（物理、化学、工程、数学、计算机等）</label>
        <br />
        <label><input type="radio" value="文科" v-model="form.major" /> 文科（中文、历史、哲学、教育学等）</label>
        <br />
        <label><input type="radio" value="社科" v-model="form.major" /> 社科（心理学、社会学、政治学等）</label>
        <br />
        <label>
          <input type="radio" value="其他" v-model="form.major" />
          其他：
          <input type="text" v-model="form.majorOther" :disabled="form.major !== '其他'" placeholder="" style="width: 120px;" />
        </label>
      </div>

      <div class="form-group">
        <label>5. 年级：</label>
        <label><input type="radio" value="大一" v-model="form.grade" required /> 大一</label>
        <label><input type="radio" value="大二" v-model="form.grade" /> 大二</label>
        <label><input type="radio" value="大三" v-model="form.grade" /> 大三</label>
        <label><input type="radio" value="大四" v-model="form.grade" /> 大四</label>
        <label><input type="radio" value="研究生" v-model="form.grade" /> 研究生</label>
      </div>

      <div class="form-group">
        <label>6. 您使用AI助手（如ChatGPT、文心一言、小爱同学等）的频率：</label>
        <label><input type="radio" value="从不" v-model="form.aiFrequency" required /> 从不</label>
        <label><input type="radio" value="很少" v-model="form.aiFrequency" /> 很少</label>
        <label><input type="radio" value="有时" v-model="form.aiFrequency" /> 有时</label>
        <label><input type="radio" value="经常" v-model="form.aiFrequency" /> 经常</label>
        <label><input type="radio" value="总是" v-model="form.aiFrequency" /> 总是</label>
      </div>

      <div class="form-group">
        <label>7. 您对AI技术的总体态度：</label><br />
        <label><input type="radio" value="非常消极" v-model="form.aiAttitude" required /> 非常消极</label><br />
        <label><input type="radio" value="比较消极" v-model="form.aiAttitude" /> 比较消极</label><br />
        <label><input type="radio" value="中性" v-model="form.aiAttitude" /> 中性</label><br />
        <label><input type="radio" value="比较积极" v-model="form.aiAttitude" /> 比较积极</label><br />
        <label><input type="radio" value="非常积极" v-model="form.aiAttitude" /> 非常积极</label>
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
        age: '',
        gender: '',
        major: '',
        majorOther: '',
        grade: '',
        aiFrequency: '',
        aiAttitude: ''
      },
      submitted: false
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
      // 处理“其他”专业
      let major = this.form.major;
      if (major === '其他' && this.form.majorOther.trim()) {
        major = this.form.majorOther.trim();
      }
      // 这里可以将数据发送到后端或做其他处理
      // console.log({
      //   ...this.form,
      //   major
      // });
      this.submitted = true;
      setTimeout(() => {
        this.$emit('submitted');
      }, 2000);
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
