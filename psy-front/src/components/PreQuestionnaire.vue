<template>
  <div class="q-bg">
    <div class="q-card">
      <h2 class="q-title">⚡ 闪电形成知识前测</h2>
      <div class="q-content">
        <!-- 指导语 -->
        <div class="q-instruction" v-if="step === 1">
          <p style="color:#2563eb;font-weight:500;margin-bottom:10px;">
            在开始学习之前，我们想了解您对闪电形成过程的现有知识。这不是考试，请根据您目前的了解如实回答。如果不知道，选择"不知道"即可。
          </p>
        </div>
        <div class="q-instruction" v-else-if="step === 2">
          <p style="color:#2563eb;font-weight:500;margin-bottom:10px;">
            请根据您的实际情况，对以下陈述进行评价。<br>
            <span style="font-size:0.98em;">（1=完全不同意，7=完全同意）</span>
          </p>
        </div>
        <div class="q-instruction" v-else-if="step === 3">
          <p style="color:#2563eb;font-weight:500;margin-bottom:10px;">
            请描述您此刻的感受程度。<br>
            <span style="font-size:0.98em;">（1=很少或没有，5=非常多）</span>
          </p>
        </div>

        <!-- Step 1: 闪电知识选择题 -->
        <div v-if="step === 1">
          <div class="q-question-block" v-for="(q, idx) in knowledgeQuestions" :key="q.id">
            <div class="q-question">
              <span class="q-qindex">{{ idx + 1 }}.</span>
              {{ q.text }}
            </div>
            <div class="q-options">
              <label v-for="opt in q.options" :key="opt.value"
                :class="['q-option', { selected: knowledgeAnswers[idx] === opt.value }]">
                <input type="radio" :value="opt.value" v-model="knowledgeAnswers[idx]" class="q-radio" />
                <span class="q-option-label">{{ opt.label }}. {{ opt.text }}</span>
              </label>
            </div>
          </div>
          <button class="q-submit-btn" @click="handleKnowledgeSubmit">提交本页</button>
        </div>

        <!-- Step 2: AI态度量表 -->
        <div v-if="step === 2">
          <div class="q-question-block" v-for="(q, idx) in aiScaleQuestions" :key="q.id">
            <div class="q-question">
              <span class="q-qindex">{{ idx + 1 }}.</span>
              {{ q.text }}
            </div>
            <div class="q-scale">
              <span class="q-scale-label">1</span>
              <div class="q-scale-options">
                <label v-for="n in 7" :key="n" :class="['q-scale-item', { selected: aiScaleAnswers[idx] === n }]">
                  <input type="radio" :value="n" v-model="aiScaleAnswers[idx]" class="q-scale-radio" />
                  <span>{{ n }}</span>
                </label>
              </div>
              <span class="q-scale-label">7</span>
            </div>
          </div>
          <!-- <div class="q-scale-summary" v-if="aiScaleScore !== null" style="margin-top:10px;color:#6366f1;">
            当前平均分：{{ aiScaleScore.toFixed(2) }}
          </div> -->
          <button class="q-submit-btn" @click="handleAIScaleSubmit">提交本页</button>
        </div>

        <!-- Step 3: 情感量表 -->
        <div v-if="step === 3">
          <div class="q-question-block" v-for="(q, idx) in affectQuestions" :key="q.id">
            <div class="q-question">
              <span class="q-qindex">{{ idx + 1 }}.</span>
              {{ q.text }}
            </div>
            <div class="q-scale">
              <span class="q-scale-label">1</span>
              <div class="q-scale-options">
                <label v-for="n in 5" :key="n" :class="['q-scale-item', { selected: affectAnswers[idx] === n }]">
                  <input type="radio" :value="n" v-model="affectAnswers[idx]" class="q-scale-radio" />
                  <span>{{ n }}</span>
                </label>
              </div>
              <span class="q-scale-label">5</span>
            </div>
          </div>
          <!-- <div class="q-scale-summary" v-if="affectPositive !== null && affectNegative !== null" style="margin-top:10px;color:#6366f1;">
            正性情感：{{ affectPositive.toFixed(2) }}
            负性情感：{{ affectNegative.toFixed(2) }}
          </div> -->
          <button class="q-submit-btn" @click="handleAffectSubmit">提交问卷</button>
        </div>

        <!-- Step 4: 结束/排除提示 -->
        <div v-if="step === 4">
          <div class="q-question-block" style="text-align:center;">
            <div v-if="excluded" style="color:#ef4444;font-weight:600;">
              很抱歉，您不符合本次实验的参与条件。<br>
              <span style="font-size:0.98em;">感谢您的配合！</span>
            </div>
            <div v-else style="color:#22c55e;font-weight:600;">
              问卷已完成，感谢您的参与！<br>
              <span style="font-size:0.98em;">请继续后续学习任务。</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import config from '@/config.js'
export default {
  name: "PreQuestionnaire",
  data() {
    return {
      step: 1,
      // Step 1: 闪电知识题
      knowledgeQuestions: [
        {
          id: 1,
          text: "您对闪电形成过程的总体了解程度：",
          options: [
            { value: "A", label: "A", text: "完全不了解，从未学过" },
            { value: "B", label: "B", text: "听说过但不清楚具体过程" },
            { value: "C", label: "C", text: "大概知道一些基本步骤" },
            { value: "D", label: "D", text: "比较清楚整个形成过程" }
          ]
        },
        {
          id: 2,
          text: "闪电形成的第一步是什么？",
          options: [
            { value: "A", label: "A", text: "冰晶碰撞产生电荷" },
            { value: "B", label: "B", text: "冷暖空气相遇，暖空气上升" },
            { value: "C", label: "C", text: "形成积雨云" },
            { value: "D", label: "D", text: "不知道" }
          ]
        },
        {
          id: 3,
          text: "暖空气为什么会上升？",
          options: [
            { value: "A", label: "A", text: "风力推动" },
            { value: "B", label: "B", text: "受热后密度变小产生浮力" },
            { value: "C", label: "C", text: "大气压力变化" },
            { value: "D", label: "D", text: "不知道" }
          ]
        },
        {
          id: 4,
          text: "积雨云是如何形成的？",
          options: [
            { value: "A", label: "A", text: "水滴不断聚集" },
            { value: "B", label: "B", text: "冰晶直接堆积" },
            { value: "C", label: "C", text: "气压变化导致" },
            { value: "D", label: "D", text: "不知道" }
          ]
        },
        {
          id: 5,
          text: "云中的电荷是如何产生的？",
          options: [
            { value: "A", label: "A", text: "冰晶相互碰撞摩擦" },
            { value: "B", label: "B", text: "温度急剧变化" },
            { value: "C", label: "C", text: "太阳辐射作用" },
            { value: "D", label: "D", text: "不知道" }
          ]
        },
        {
          id: 6,
          text: "为什么云层会形成上下电荷分布？",
          options: [
            { value: "A", label: "A", text: "重力作用使不同电荷分离" },
            { value: "B", label: "B", text: "地球磁场影响" },
            { value: "C", label: "C", text: "风力吹散电荷" },
            { value: "D", label: "D", text: "不知道" }
          ]
        },
        {
          id: 7,
          text: "空气什么时候会被\"击穿\"？",
          options: [
            { value: "A", label: "A", text: "电场强度超过临界值" },
            { value: "B", label: "B", text: "温度过高时" },
            { value: "C", label: "C", text: "湿度过大时" },
            { value: "D", label: "D", text: "不知道" }
          ]
        },
        {
          id: 8,
          text: "闪电放电的本质是什么？",
          options: [
            { value: "A", label: "A", text: "积累的电荷快速中和" },
            { value: "B", label: "B", text: "空气分子燃烧" },
            { value: "C", label: "C", text: "磁场突然变化" },
            { value: "D", label: "D", text: "不知道" }
          ]
        }
      ],
      knowledgeAnswers: Array(8).fill(""),
      // Step 2: AI态度量表
      aiScaleQuestions: [
        { id: 1, text: "我经常使用AI助手（如ChatGPT、Siri、小爱同学等）" },
        { id: 2, text: "我对AI技术比较熟悉" },
        { id: 3, text: "我认为AI技术很有用" },
        { id: 4, text: "我愿意尝试新的AI产品" },
        { id: 5, text: "我对AI技术持积极态度" }
      ],
      aiScaleAnswers: Array(5).fill(null),
      // Step 3: 情感量表
      affectQuestions: [
        { id: 1, text: "目前您感到多大程度的：兴奋的" },
        { id: 2, text: "目前您感到多大程度的：热情的" },
        { id: 3, text: "目前您感到多大程度的：警觉的" },
        { id: 4, text: "目前您感到多大程度的：沮丧的" },
        { id: 5, text: "目前您感到多大程度的：烦躁的" }
      ],
      affectAnswers: Array(5).fill(null),
      // 结束/排除
      excluded: false,
      submitting: false
    };
  },
  created() {
    this.$nextTick(() => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  },
  computed: {
    // AI态度量表平均分
    aiScaleScore() {
      if (this.aiScaleAnswers.some(v => v === null)) return null;
      const sum = this.aiScaleAnswers.reduce((a, b) => a + b, 0);
      return sum / this.aiScaleAnswers.length;
    },
    // 情感量表分数
    affectPositive() {
      if (this.affectAnswers.slice(0, 3).some(v => v === null)) return null;
      return (
        (this.affectAnswers[0] + this.affectAnswers[1] + this.affectAnswers[2]) / 3
      );
    },
    affectNegative() {
      if (this.affectAnswers.slice(3, 5).some(v => v === null)) return null;
      return (
        (this.affectAnswers[3] + this.affectAnswers[4]) / 2
      );
    }
  },
  methods: {
    // Step 1: 知识题提交
    handleKnowledgeSubmit() {
      // 检查是否全部作答
      if (this.knowledgeAnswers.some(ans => !ans)) {
        alert("请完整填写所有问题后再提交！");
        return;
      }
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
      this.step = 2;
      this.$nextTick(() => {
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
    },
    // Step 2: AI态度量表提交
    handleAIScaleSubmit() {
      if (this.aiScaleAnswers.some(ans => ans === null)) {
        alert("请完整填写所有问题后再提交！");
        return;
      }
      this.step = 3;
      this.$nextTick(() => {
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
    },
    // Step 3: 情感量表提交
    handleAffectSubmit() {
      if (this.affectAnswers.some(ans => ans === null)) {
        alert("请完整填写所有问题后再提交！");
        return;
      }
      this.excluded = false;
      this.submitAllQuestionnaireData(false);
    },
    // 提交所有问卷数据到后端
    async submitAllQuestionnaireData(isExcluded) {
      if (this.submitting) return;
      this.submitting = true;
      try {
        // 获取用户id（假设已存于store）
        const userId = this.$store.state.userInfo?.id || '';
        const userName = this.$store.state.userInfo?.name || '';
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

        // 组装知识题详细答案
        const knowledgeDetail = this.knowledgeQuestions.map((q, idx) => {
          const selected = this.knowledgeAnswers[idx];
          return {
            id: q.id,
            text: q.text,
            selectedValue: selected,
            selectedLabel: (q.options.find(opt => opt.value === selected) || {}).label || '',
            selectedText: (q.options.find(opt => opt.value === selected) || {}).text || ''
          }
        });

        // 组装AI态度量表详细答案
        const aiScaleDetail = this.aiScaleQuestions.map((q, idx) => {
          const selected = this.aiScaleAnswers[idx];
          return {
            id: q.id,
            text: q.text,
            selectedScore: selected
          }
        });

        // 组装情感量表详细答案
        const affectDetail = this.affectQuestions.map((q, idx) => {
          const selected = this.affectAnswers[idx];
          return {
            id: q.id,
            text: q.text,
            selectedScore: selected
          }
        });

        // 组装payload
        const payload = {
          userId,
          userName,
          time,
          excluded: isExcluded,
          knowledge: {
            answers: this.knowledgeAnswers.slice(),
            detail: knowledgeDetail
          },
          aiScale: {
            answers: this.aiScaleAnswers.slice(),
            detail: aiScaleDetail,
            score: this.aiScaleScore
          },
          affect: {
            answers: this.affectAnswers.slice(),
            detail: affectDetail,
            positive: this.affectPositive,
            negative: this.affectNegative
          }
        };
        // 提交到自定义url
        const url = `${config.apiBaseUrl}/pre_questionnaire`;
        await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });
        // 可选：处理成功/失败
      } catch (e) {
        // 可选：处理错误
        console.error('问卷提交失败', e);
      } finally {
        this.submitting = false;
        this.step = 4;
        this.$store.commit('setStateToNext', { currentState: this.$store.state.flowState, delay: 2000 });
      }
    }
  }
};
</script>