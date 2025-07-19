<template>
  <div class="questionnaire-bg">
    <div class="questionnaire-card">
      <h2 class="pq-title">⚡ 闪电形成知识后测</h2>
      <div class="pq-content">
        <!-- 阶段1：主观体验量表 -->
        <div v-if="step === 1">
          <div class="pq-instruction">
            <b>指导语：</b>以下是多个关于你在使用AI学习助手时的主观感受与体验的陈述，请根据你的真实体验，从1=“完全不同意”到5=“完全同意”中选择一个最符合你感受的选项。
          </div>
          <div v-for="(group, gIdx) in subjectiveGroups" :key="gIdx" class="pq-scale-group">
            <div class="pq-scale-group-title">{{ group.title }}</div>
            <div v-for="(q, qIdx) in group.questions" :key="qIdx" class="pq-question-block">
              <div class="pq-question">
                <span class="pq-qindex">{{ group.base + qIdx + 1 }}.</span>
                {{ q.text }}
              </div>
              <div class="pq-scale">
                <span class="pq-scale-label">1</span>
                <div class="pq-scale-options pq-scale-5">
                  <label v-for="n in 5" :key="n"
                    :class="['pq-scale-item', { selected: subjectiveAnswers[group.base + qIdx] === n }]">
                    <input type="radio" :value="n" v-model="subjectiveAnswers[group.base + qIdx]"
                      class="pq-scale-radio" />
                    <span>{{ n }}</span>
                  </label>
                </div>
                <span class="pq-scale-label">5</span>
              </div>
            </div>
          </div>
          <button class="pq-submit-btn" @click="handleSubjectiveSubmit">提交本部分</button>
        </div>

        <!-- 阶段2：知识题 -->
        <div v-else-if="step === 2">
          <div class="pq-instruction">
            <b>指导语：</b>请根据刚才的学习内容，回答以下问题。
          </div>
          <div v-for="(q, idx) in knowledgeQuestions" :key="idx" class="pq-question-block">
            <div class="pq-question">
              <span class="pq-qindex">{{ idx + 1 }}.</span>
              {{ q.text }}
            </div>
            <div v-if="q.type === 'choice'" class="pq-options">
              <label v-for="opt in q.options" :key="opt.value"
                :class="['pq-option', { selected: knowledgeAnswers[idx] === opt.value }]">
                <input type="radio" :value="opt.value" v-model="knowledgeAnswers[idx]" class="pq-radio" />
                <span class="pq-option-label">{{ opt.label }}. {{ opt.text }}</span>
              </label>
            </div>
          </div>
          <button class="pq-submit-btn" @click="handleKnowledgeSubmit">提交本部分</button>
        </div>

        <!-- 阶段3：系统体验量表与开放题 -->
        <div v-else-if="step === 3">
          <div class="pq-instruction">
            <b>指导语：</b>请对您刚才使用AI学习系统的体验进行评价。（1=完全不同意，7=完全同意）
          </div>
          <div v-for="(group, gIdx) in systemGroups" :key="gIdx" class="pq-scale-group">
            <div class="pq-scale-group-title">{{ group.title }}</div>
            <div v-for="(q, qIdx) in group.questions" :key="qIdx" class="pq-question-block">
              <div class="pq-question">
                <span class="pq-qindex">{{ group.base + qIdx + 1 }}.</span>
                {{ q.text }}
              </div>
              <div class="pq-scale">
                <span class="pq-scale-label">1</span>
                <div class="pq-scale-options">
                  <label v-for="n in 7" :key="n"
                    :class="['pq-scale-item', { selected: systemAnswers[group.base + qIdx] === n }]">
                    <input type="radio" :value="n" v-model="systemAnswers[group.base + qIdx]" class="pq-scale-radio" />
                    <span>{{ n }}</span>
                  </label>
                </div>
                <span class="pq-scale-label">7</span>
              </div>
            </div>
          </div>
          <div class="pq-question-block">
            <div class="pq-question">
              <span class="pq-qindex">10.</span>
              您对这个AI学习系统的总体印象是什么？（请简述）
            </div>
            <textarea v-model="systemOpen1" class="pq-textarea" rows="3" placeholder="请输入您的看法..."></textarea>
          </div>
          <div class="pq-question-block">
            <div class="pq-question">
              <span class="pq-qindex">11.</span>
              您觉得这个系统还可以在哪些方面改进？（请简述）
            </div>
            <textarea v-model="systemOpen2" class="pq-textarea" rows="3" placeholder="请输入您的建议..."></textarea>
          </div>
          <button class="pq-submit-btn" @click="handleSystemSubmit">提交全部问卷</button>
        </div>

        <!-- 阶段4：结果展示 -->
        <div v-else-if="step === 4" class="pq-result">
          <h3>🎉 问卷已提交！</h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import config from '@/config.js'
export default {
  name: "PostQuestionnaire",
  data() {
    return {
      step: 1,
      // 主观体验量表
      subjectiveGroups: [
        {
          title: "社交性",
          base: 0,
          questions: [
            { text: "它的自我介绍和称呼方式让我感觉像在和一个人打招呼。" },
            { text: "它的问候语和用词让我觉得像是在与真实的人交流。" },
            { text: "和它互动时，我会感受到一种温暖的感觉。" },
            { text: "在学习过程中，它总是表现得亲切而友好。" }
          ]
        },
        {
          title: "生命感（Animacy）",
          base: 4,
          questions: [
            { text: "即使没跟它说话，只看它的样子也让我觉得它不是那种死板的程序。" },
            { text: "它给我的感觉更像一个会表达、会互动的角色，而不是一个纯粹的工具。" },
            { text: "和它交流时，我会觉得像是在和一个真实的人说话。" },
            { text: "它的表达方式生动自然，不像机器一板一眼地回应。" }
          ]
        },
        {
          title: "能动性（Agency）",
          base: 8,
          questions: [
            { text: "它的回答让我觉得它有自己的思考过程。" },
            { text: "它帮助我的方式不像是在执行预设程序，更像是出于自己的判断。" },
            { text: "它在解决问题时，会自己分析，而不是一成不变地回答。" }
          ]
        },
        {
          title: "教学支持（Teaching Support）",
          base: 11,
          questions: [
            { text: "它的用语和表达方式让我觉得它像一位真正的老师。" },
            { text: "它会根据我的学习进展灵活调整回答方式。" },
            { text: "它对我的表现显得贴心和耐心，让我感觉得像被老师关心着一样。" }
          ]
        },
        {
          title: "干扰性（Disturbance）",
          base: 14,
          questions: [
            { text: "它的外表让我觉得有点奇怪、不太自然。" },
            { text: "它与我互动时模仿人类情感表达的方式，让我觉得反感。" },
            { text: "它展现智能的方式有时像人，有时又不像人，这种感觉让我不适。" },
            { text: "它模仿人类行为的方式让我觉得有些别扭。" }
          ]
        }
      ],
      subjectiveAnswers: Array(18).fill(null),

      // 知识题
      knowledgeQuestions: [
        // 概念理解 1-8
        {
          text: "闪电形成的第一步是：",
          type: "choice",
          options: [
            { value: "A", label: "A", text: "冰晶碰撞产生电荷" },
            { value: "B", label: "B", text: "冷暖空气相遇，暖空气上升" },
            { value: "C", label: "C", text: "形成积雨云" },
            { value: "D", label: "D", text: "电场击穿空气" }
          ]
        },
        {
          text: "暖空气上升的根本原因是：",
          type: "choice",
          options: [
            { value: "A", label: "A", text: "风力推动" },
            { value: "B", label: "B", text: "密度差异产生浮力" },
            { value: "C", label: "C", text: "大气压力变化" },
            { value: "D", label: "D", text: "地球重力减弱" }
          ]
        },
        {
          text: "水蒸气在高空凝结的主要原因是：",
          type: "choice",
          options: [
            { value: "A", label: "A", text: "气压降低" },
            { value: "B", label: "B", text: "温度降低达到饱和点" },
            { value: "C", label: "C", text: "紫外线作用" },
            { value: "D", label: "D", text: "风速增大" }
          ]
        },
        {
          text: "积雨云的形成过程是：",
          type: "choice",
          options: [
            { value: "A", label: "A", text: "小水滴碰撞聚合" },
            { value: "B", label: "B", text: "冰晶直接堆积" },
            { value: "C", label: "C", text: "气压突变导致" },
            { value: "D", label: "D", text: "温度骤降形成" }
          ]
        },
        {
          text: "云中电荷产生的机制是：",
          type: "choice",
          options: [
            { value: "A", label: "A", text: "冰晶相互碰撞摩擦" },
            { value: "B", label: "B", text: "温度梯度作用" },
            { value: "C", label: "C", text: "重力分离效应" },
            { value: "D", label: "D", text: "磁场感应作用" }
          ]
        },
        {
          text: "云层电荷分布的特点是：",
          type: "choice",
          options: [
            { value: "A", label: "A", text: "顶部负电荷，底部正电荷" },
            { value: "B", label: "B", text: "顶部正电荷，底部负电荷" },
            { value: "C", label: "C", text: "电荷均匀分布" },
            { value: "D", label: "D", text: "随机分布" }
          ]
        },
        {
          text: "空气被击穿的条件是：",
          type: "choice",
          options: [
            { value: "A", label: "A", text: "温度超过100°C" },
            { value: "B", label: "B", text: "电场强度超过阈值" },
            { value: "C", label: "C", text: "湿度达到100%" },
            { value: "D", label: "D", text: "气压降到最低" }
          ]
        },
        {
          text: "闪电放电的本质是：",
          type: "choice",
          options: [
            { value: "A", label: "A", text: "空气分子燃烧" },
            { value: "B", label: "B", text: "电荷快速中和" },
            { value: "C", label: "C", text: "磁场突然变化" },
            { value: "D", label: "D", text: "重力场扭曲" }
          ]
        },
        // 应用理解 9-10
        {
          text: "如果没有温度梯度，闪电还能形成吗？为什么？",
          type: "choice",
          options: [
            { value: "A", label: "A", text: "能，因为电荷分离不依赖温度" },
            { value: "B", label: "B", text: "不能，因为没有上升气流" },
            { value: "C", label: "C", text: "能，风力可以替代" },
            { value: "D", label: "D", text: "不确定" }
          ]
        },
        {
          text: "为什么沙漠地区很少发生雷暴？",
          type: "choice",
          options: [
            { value: "A", label: "A", text: "沙漠没有水汽" },
            { value: "B", label: "B", text: "温差不够大" },
            { value: "C", label: "C", text: "缺乏对流条件" },
            { value: "D", label: "D", text: "电阻率太高" }
          ]
        },
        // 知识迁移 11-12
        {
          text: "基于闪电形成原理，高楼更容易被雷击的原因是：",
          type: "choice",
          options: [
            { value: "A", label: "A", text: "高楼材料导电性好" },
            { value: "B", label: "B", text: "高楼提供了更短的放电路径" },
            { value: "C", label: "C", text: "高楼产生电磁场" },
            { value: "D", label: "D", text: "高楼改变气流方向" }
          ]
        },
        {
          text: "人工引发闪电现象的可能方法是：",
          type: "choice",
          options: [
            { value: "A", label: "A", text: "增加空气湿度" },
            { value: "B", label: "B", text: "用火箭拖拽导线到云中" },
            { value: "C", label: "C", text: "发射激光束" },
            { value: "D", label: "D", text: "释放带电粒子" }
          ]
        }
      ],
      knowledgeAnswers: Array(12).fill(""),

      // 系统体验量表与开放题
      systemGroups: [
        {
          title: "继续使用意愿",
          base: 0,
          questions: [
            { text: "如果有机会，我愿意继续使用这个AI学习系统" },
            { text: "我会向同学推荐这个AI学习系统" },
            { text: "我希望学校采用类似的AI教学系统" }
          ]
        },
        {
          title: "学习满意度",
          base: 3,
          questions: [
            { text: "我对这次的AI学习体验感到满意" },
            { text: "这个AI系统帮助我有效学习了闪电知识" },
            { text: "我觉得用AI学习比传统方式更有趣" }
          ]
        },
        {
          title: "系统易用性",
          base: 6,
          questions: [
            { text: "这个AI系统很容易使用" },
            { text: "我的操作能够被系统准确理解" },
            { text: "系统的反馈及时且有用" }
          ]
        }
      ],
      systemAnswers: Array(9).fill(null),
      systemOpen1: "",
      systemOpen2: "",

      // 结果
      knowledgeScore: 0,
      knowledgeSubScores: {
        concept: 0,
        application: 0,
        transfer: 0
      },
      willContinueScore: 0,
      satisfactionScore: 0,
      usabilityScore: 0,
    };
  },
  methods: {
    handleSubjectiveSubmit() {
      if (this.subjectiveAnswers.some(ans => ans === null)) {
        alert("请完成所有主观体验量表题目后再提交！");
        return;
      }
      // 提交主观体验量表到后端，同时提交所有题目内容
      self.subjective_payload = {
        questions: this.subjectiveGroups.flatMap(g => g.questions.map(q => q.text)),
        answers: this.subjectiveAnswers,
      };
      this.step++;
      this.$nextTick(() => {
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
    },
    handleKnowledgeSubmit() {
      if (this.knowledgeAnswers.some(ans => !ans)) {
        alert("请完成所有知识题后再提交！");
        return;
      }
      // 计分
      const correct = ["B", "B", "B", "A", "A", "B", "B", "B", "B", "C", "B", "B"];
      let concept = 0, application = 0, transfer = 0;
      for (let i = 0; i < 8; i++) if (this.knowledgeAnswers[i] === correct[i]) concept++;
      for (let i = 8; i < 10; i++) if (this.knowledgeAnswers[i] === correct[i]) application++;
      for (let i = 10; i < 12; i++) if (this.knowledgeAnswers[i] === correct[i]) transfer++;
      this.knowledgeSubScores = { concept, application, transfer };
      this.knowledgeScore = concept + application + transfer;

      // 提交知识题到后端，同时提交所有题目内容和选项
      const questions = this.knowledgeQuestions.map(q => ({
        text: q.text,
        options: q.options ? q.options.map(opt => ({
          value: opt.value,
          label: opt.label,
          text: opt.text
        })) : []
      }));
      self.knowledge_payload = {
        questions: questions,
        answers: this.knowledgeAnswers,
        score: this.knowledgeScore,
        subScores: this.knowledgeSubScores,
        timestamp: Date.now()
      };
      this.step++;
      this.$nextTick(() => {
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
    },
    handleSystemSubmit() {
      if (this.systemAnswers.some(ans => ans === null) || !this.systemOpen1.trim() || !this.systemOpen2.trim()) {
        alert("请完整填写所有系统体验题目和简答题后再提交！");
        return;
      }
      // 计分
      this.willContinueScore = (this.systemAnswers[0] + this.systemAnswers[1] + this.systemAnswers[2]) / 3;
      this.satisfactionScore = (this.systemAnswers[3] + this.systemAnswers[4] + this.systemAnswers[5]) / 3;
      this.usabilityScore = (this.systemAnswers[6] + this.systemAnswers[7] + this.systemAnswers[8]) / 3;

      // 提交系统体验量表与开放题到后端，同时提交所有题目内容
      const questions = this.systemGroups.flatMap(g => g.questions.map(q => q.text));
      self.system_payload = {
        questions: questions,
        answers: this.systemAnswers,
        open1: this.systemOpen1,
        open2: this.systemOpen2,
        willContinueScore: this.willContinueScore,
        satisfactionScore: this.satisfactionScore,
        usabilityScore: this.usabilityScore,
        timestamp: Date.now()
      };
    },
  },
  async submitAllQuestionnaireData() {
    const now = new Date();
    const pad = n => n.toString().padStart(2, '0');
    const time =
      now.getFullYear() + '-' +
      pad(now.getMonth() + 1) + '-' +
      pad(now.getDate()) + ' ' +
      pad(now.getHours()) + ':' +
      pad(now.getMinutes()) + ':' +
      pad(now.getSeconds());

    const payload = {
      userId: this.$store.state.userInfo?.id || '',
      userName: this.$store.state.userInfo?.name || '',
      time,
      subjective: self.subjective_payload,
      knowledge: self.knowledge_payload,
      system: self.system_payload
    }
    let success = false;
    let attempts = 0;
    let lastError = null;
    while (!success && attempts < 5) {
      try {
        const res = await fetch(`${config.apiBaseUrl}/post_questionnaire`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error('Network response was not ok');
        success = true;
      } catch (e) {
        lastError = e;
        attempts++;
        if (attempts < 5) {
          await new Promise(resolve => setTimeout(resolve, 1000));
        }
      }
    }
    if (success) {
      this.step++;
      this.$store.commit('setStateToNext', { currentState: this.$store.state.flowState, delay: 2000 });
    } else {
      alert('问卷提交失败，请检查网络后重试。');
      // 可选：你可以在这里做进一步的错误处理
      console.error('问卷提交失败', lastError);
    }
  }
};
</script>

<style scoped>
.pq-instruction {
  background: #f6f8fa;
  border-left: 4px solid #4e8cff;
  padding: 10px 16px;
  margin-bottom: 18px;
  font-size: 15px;
  color: #333;
}

.pq-scale-group-title {
  font-weight: bold;
  margin: 18px 0 8px 0;
  color: #2a5db0;
}

.pq-scale-5 .pq-scale-item {
  width: 32px;
}

.pq-result {
  text-align: center;
  padding: 24px 0;
}

.pq-score-block {
  margin: 12px 0;
  font-size: 16px;
}
</style>