<template>
  <div class="q-bg">
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
      <h2 class="q-title">⚡ 闪电形成知识前测</h2>
      <div class="q-content">
        <!-- Step 1: 闪电知识选择题 -->
        <div v-if="step === 1">
          <div class="q-instruction">
            在开始学习之前，我们想了解您对闪电形成过程的现有知识。这不是考试，请根据您目前的了解如实回答。如果不知道，选择"不知道"即可。
          </div>
          <SelectQuestion :questions="knowledgeQuestions" v-model="knowledgeAnswers"/>
          <button class="q-submit-btn" @click="handleKnowledgeSubmit">提交本部分</button>
        </div>

        <!-- Step 2: AI态度量表 -->
        <div v-if="step === 2">
          <div class="q-instruction">
            请根据您的实际情况，对以下陈述进行评价。（1=完全不同意，7=完全同意）
          </div>
          <ScaleQuestion :questions="aiScaleQuestions" :max="7" v-model="aiScaleAnswers"/>
          <button class="q-submit-btn" @click="handleAIScaleSubmit">提交本部分</button>
        </div>

        <!-- Step 3: 情感量表 -->
        <div v-if="step === 3">
          <div class="q-instruction">
            请描述您此刻的感受程度。（1=很少或没有，5=非常多）
          </div>
          <ScaleQuestion :questions="affectQuestions" :max="5" v-model="affectAnswers"/>
          <button class="q-submit-btn" @click="handleAffectSubmit">提交全部</button>
        </div>

        <!-- Step 4: 结束/排除提示 -->
        <div v-if="step === 4">
          <div class="q-question-block" style="text-align:center;">
            <div v-if="excluded" style="color:#ef4444;font-weight:600;">
              很抱歉，您不符合本次实验的参与条件。<br>
              <span style="font-size:0.98em;">感谢您的配合！</span>
            </div>
            <div v-else style="color:#22c55e;font-weight:600;">
              问卷已完成！<br>
              <span style="font-size:0.98em;">请继续后续学习任务。</span>
            </div>
          </div>
        </div>


      </div>
    </div>
  </div>
</template>

<script>
import ScaleQuestion from './components/ScaleQuestion.vue';
import SelectQuestion from './components/SelectQuestion.vue';
import { checkFill, checkFillStep, step } from '@/tools';
export default {
  name: "PreQuestionnaire",
  components: {ScaleQuestion, SelectQuestion},
  data() {
    return {
      check: true,
      step: 1,
      // Step 1: 闪电知识题
      knowledgeQuestions: [
        {
          text: "您对闪电形成过程的总体了解程度：",
          options: [
            { value: "A", text: "完全不了解，从未学过" },
            { value: "B", text: "听说过但不清楚具体过程" },
            { value: "C", text: "大概知道一些基本步骤" },
            { value: "D", text: "比较清楚整个形成过程" }
          ]
        },
        {
          text: "闪电形成的第一步是什么？",
          options: [
            { value: "A", text: "冰晶碰撞产生电荷" },
            { value: "B", text: "冷暖空气相遇，暖空气上升" },
            { value: "C", text: "形成积雨云" },
            { value: "D", text: "不知道" }
          ]
        },
        {
          text: "暖空气为什么会上升？",
          options: [
            { value: "A", text: "风力推动" },
            { value: "B", text: "受热后密度变小产生浮力" },
            { value: "C", text: "大气压力变化" },
            { value: "D", text: "不知道" }
          ]
        },
        {
          text: "积雨云是如何形成的？",
          options: [
            { value: "A", text: "水滴不断聚集" },
            { value: "B", text: "冰晶直接堆积" },
            { value: "C", text: "气压变化导致" },
            { value: "D", text: "不知道" }
          ]
        },
        {
          text: "云中的电荷是如何产生的？",
          options: [
            { value: "A", text: "冰晶相互碰撞摩擦" },
            { value: "B", text: "温度急剧变化" },
            { value: "C", text: "太阳辐射作用" },
            { value: "D", text: "不知道" }
          ]
        },
        {
          text: "为什么云层会形成上下电荷分布？",
          options: [
            { value: "A", text: "重力作用使不同电荷分离" },
            { value: "B", text: "地球磁场影响" },
            { value: "C", text: "风力吹散电荷" },
            { value: "D", text: "不知道" }
          ]
        },
        {
          text: "空气什么时候会被\"击穿\"？",
          options: [
            { value: "A", text: "电场强度超过临界值" },
            { value: "B", text: "温度过高时" },
            { value: "C", text: "湿度过大时" },
            { value: "D", text: "不知道" }
          ]
        },
        {
          text: "闪电放电的本质是什么？",
          options: [
            { value: "A", text: "积累的电荷快速中和" },
            { value: "B", text: "空气分子燃烧" },
            { value: "C", text: "磁场突然变化" },
            { value: "D", text: "不知道" }
          ]
        }
      ],
      knowledgeAnswers: Array(8).fill(""),
      // Step 2: AI态度量表
      aiScaleQuestions: [
        { text: "我经常使用AI助手（如ChatGPT、Siri、小爱同学等）" },
        { text: "我对AI技术比较熟悉" },
        { text: "我认为AI技术很有用" },
        { text: "我愿意尝试新的AI产品" },
      ],
      aiScaleAnswers: Array(4).fill(null),
      // Step 3: 情感量表
      affectQuestions: [
        { text: "兴奋的" },
        { text: "热情的" },
        { text: "享受的" },
        { text: "好奇的" },
        { text: "沮丧的" },
        { text: "焦虑的" },
        { text: "无聊的" },
        { text: "困惑的" },
      ],
      affectAnswers: Array(8).fill(null),
      // 结束/排除
      excluded: false,
      submitting: false,
      errorMessage: '',
    };
  },
  created() {
    this.$nextTick(() => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  },
  methods: {
    // Step 1: 知识题提交
    handleKnowledgeSubmit() {
      // 检查是否全部作答
      if (!checkFill(this, this.knowledgeAnswers)) return
      // 排除标准
      // 1. 选择A/B/C的题目超过4题（50%），排除
      // 2. 第1题选择C或D，排除
      const abcCount = this.knowledgeAnswers.filter(ans => ["A", "B", "C"].includes(ans)).length;
      const q1 = this.knowledgeAnswers[0];
      if (abcCount > 4 || q1 === "C" || q1 === "D") {
        this.excluded = true;
        this.step = 4;
        this.$nextTick(() => {
          window.scrollTo({ top: 0, behavior: "smooth" });
        });
        // 依然提交数据到后端，标记为排除
        this.submitAllQuestionnaireData(true);
        return;
      }
      // 通过，进入下一步
      step(this)
    },
    // Step 2: AI态度量表提交
    handleAIScaleSubmit() {
      checkFillStep(this, this.aiScaleAnswers)
    },
    // Step 3: 情感量表提交
    handleAffectSubmit() {
      if (!checkFill(this, this.affectAnswers)) return
      this.excluded = false;
      this.submitAllQuestionnaireData(false);
    },
    // 提交所有问卷数据到后端
    async submitAllQuestionnaireData(isExcluded) {
      if (this.submitting) return;
      this.submitting = true;
      
      // 获取用户id（假设已存于store）
      const userId = this.$store.state.userInfo?.userId || '';
      const userName = this.$store.state.userInfo?.userName || '';
      // 时间戳
      const now = new Date();
      const pad = n => n.toString().padStart(2, '0');
      const time =
        now.getFullYear() + '-' +
        pad(now.getMonth() + 1) + '-' +
        pad(now.getDate()) + ' ' +
        pad(now.getHours()) + ':' +
        pad(now.getMinutes()) + ':' +
        pad(now.getSeconds());

      // 组装payload
      const payload = {
        userId,
        userName,
        time,
        excluded: isExcluded,
        knowledgePayload: {
          questions: this.knowledgeQuestions,
          answers: this.knowledgeAnswers.slice(),
        },
        aiScalePayload: {
          questions: this.aiScaleQuestions,
          answers: this.aiScaleAnswers.slice(),
          score: this.aiScaleAnswers.reduce((a, b) => a + b, 0) / this.aiScaleAnswers.length,
        },
        affectPayload: {
          questions: this.affectQuestions,
          answers: this.affectAnswers.slice(),
          positive: this.affectAnswers.slice(0, 4).reduce((sum, val) => sum + val, 0) / this.affectAnswers.length * 2,
          negative: this.affectAnswers.slice(4, 8).reduce((sum, val) => sum + val, 0) / this.affectAnswers.length * 2,
        }
      };
      this.$ws.send(JSON.stringify({
        type: 'pre_questionnaire',
        data: payload
      }))
      step(this)
      this.$store.commit('setStateToNext', { currentState: this.$store.state.flowState, delay: 2000 });
    },
    showError(msg) {
      this.errorMessage = msg;
    }
  }
};
</script>