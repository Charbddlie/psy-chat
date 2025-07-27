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
      <h2 class="q-title">⚡ 闪电形成知识后测</h2>
      <div class="q-content">
        <!-- step 1: PANAS正负情感量表 -->
        <div v-if="step === 1">
          <div class="q-instruction">
            在刚才与AI学习助手交互后，您现在感到多大程度的：
          </div>
          <ScaleQuestion :questions="affectQuestions" :max="5" v-model="affectAnswers"/>
          <button class="q-submit-btn" @click="handleAffectSubmit">提交本部分</button>
        </div>
        <!-- step 2：AI拟人化感知量表 -->
        <div v-else-if="step === 2">
          <div class="q-instruction">
            以下是多个关于你在使用AI学习助手时的主观感受与体验的陈述，请根据你的真实体验，从1=“完全不同意”到5=“完全同意”中选择一个最符合你感受的选项。
          </div>
          <ScaleQuestion :questions="subjectiveQuestions" :max="5" v-model="subjectiveAnswers"/>
          <button class="q-submit-btn" @click="handleSubjectiveSubmit">提交本部分</button>
        </div>
        
        <!-- step 3：Godspeed量表简化版 -->
        <div v-else-if="step === 3">
          <div class="q-instruction">
            请根据您刚才与AI学习助手的交互体验，在以下每对词语之间选择最符合您感受的数字。数字越接近某个词语，表示AI助手越接近该特征。以 "假的 1--2--3--4--5--6--7 自然的" 为例: 1 = 完全是假的 -> 7 = 完全自然的
          </div>
          <ScaleQuestion :questions="godQuestions" :max="7" v-model="godAnswers"/>
          <button class="q-submit-btn" @click="handleGodSubmit">提交本部分</button>
        </div>
        
        <!-- step 4：学习效果测试 -->
        <div v-else-if="step === 4">
          <div class="q-instruction">
            请根据刚才的学习内容，回答以下问题。
          </div>
          <SelectQuestion :questions="knowledgeQuestions" v-model="knowledgeAnswers"/>
          <button class="q-submit-btn" @click="handleKnowledgeSubmit">提交本部分</button>
        </div>
        
        <!-- step 5：认知负荷量表 -->
        <div v-else-if="step === 5">
          <div class="q-instruction">
            在刚才的AI学习过程中，您感到（7点量表：1=非常低，7=非常高）：
          </div>
          <ScaleQuestion :questions="cogQuestions" :max="7" v-model="cogAnswers"/>
          <button class="q-submit-btn" @click="handleCogSubmit">提交本部分</button>
        </div>
        
        <!-- step 6：系统体验量表与开放题 -->
        <div v-else-if="step === 6">
          <div class="q-instruction">
            请对您刚才使用AI学习系统的体验进行评价。（1=完全不同意，7=完全同意）
          </div>
          <ScaleQuestion :questions="systemQuestions" :max="7" v-model="systemAnswers"/>
          <button class="q-submit-btn" @click="handleSystemSubmit">提交本部分</button>
        </div>
        
        <!-- step 7：社会临场感 -->
        <div v-else-if="step === 7">
          <div class="q-instruction">
            关于刚才与AI学习助手的交互体验（7点量表：1=完全不同意，7=完全同意）：
          </div>
          <ScaleQuestion :questions="socialQuestions" :max="7" v-model="socialAnswers"/>
          <button class="q-submit-btn" @click="handleSocialSubmit">提交本部分</button>
        </div>
        <!-- step 8：技术信任量表 -->
        <div v-else-if="step === 8">
          <div class="q-instruction">
            对于刚才使用的AI学习助手（7点量表：1=完全不同意，7=完全同意）：
          </div>
          <ScaleQuestion :questions="techQuestions" :max="7" v-model="techAnswers"/>
          <button class="q-submit-btn" @click="handleTechSubmit">提交全部</button>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import ScaleQuestion from './components/ScaleQuestion.vue';
import SelectQuestion from './components/SelectQuestion.vue';
import { checkFill, checkFillStep } from '@/tools';
export default {
  name: "PostQuestionnaire",
  components: {ScaleQuestion, SelectQuestion},
  data() {
    return {
      check: true,
      step: 3,
      // step 0: 情感量表
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
      // 主观体验量表
      subjectiveQuestions: [
        { text: "它的自我介绍和称呼方式让我感觉像在和一个人打招呼。" },
        { text: "它的交互方式让我觉得很自然。" },
        { text: "和它互动时，我会感受到一种温暖的感觉。" },
        { text: "在学习过程中，它总是表现得亲切而友好。" },
        { text: "它不是一个死板的程序。" },
        { text: "它给我的感觉更像一个会主动表达互动的角色，而不是一个纯粹的工具。" },
        { text: "和它交流时，我会觉得像是在和一个真实的人说话。" },
        { text: "它的表达方式生动自然，不像机器一板一眼地回应。" },
        { text: "它的回答让我觉得它有自己的思考过程。" },
        { text: "它帮助我的方式不像是在执行预设程序，更像是出于自己的判断。" },
        { text: "它在解决问题时，会自己分析，而不是一成不变地回答。" },
        { text: "它的用语和表达方式让我觉得它像一位真正的老师。" },
        { text: "它会根据我的学习问题灵活调整回答方式。" },
        { text: "它对我的表现显得贴心和耐心，让我感觉得像被老师关心着一样。" },
        { text: "它的表现让我觉得有点奇怪、不太自然。" },
        { text: "它与我互动时模仿人类情感表达的方式，让我觉得反感。" },
        { text: "它展现智能的方式有时像人，有时又不像人，这种感觉让我不适。" },
        { text: "它模仿人类行为的方式让我觉得有些别扭。" },
      ],
      subjectiveAnswers: Array(18).fill(null),
      godQuestions: [
        { text: "假的/自然的" },
        { text: "机器化的/人性化的" },
        { text: "死板的/生动的" },
        { text: "机械的/有生命的" },
        { text: "不友好的/友好的" },
        { text: "不友善的/友善的" },
      ],
      godAnswers: Array(6).fill(null),
      // 知识题
      knowledgeQuestions: [
        // 概念理解 1-8
        {
          text: "闪电形成的第一步是：",
          options: [
            { value: "A", text: "冰晶碰撞产生电荷" },
            { value: "B", text: "冷暖空气相遇，暖空气上升" },
            { value: "C", text: "形成积雨云" },
            { value: "D", text: "电场击穿空气" }
          ]
        },
        {
          text: "暖空气上升的根本原因是：",
          options: [
            { value: "A", text: "风力推动" },
            { value: "B", text: "密度差异产生浮力" },
            { value: "C", text: "大气压力变化" },
            { value: "D", text: "地球重力减弱" }
          ]
        },
        {
          text: "水蒸气在高空凝结的主要原因是：",
          options: [
            { value: "A", text: "气压降低" },
            { value: "B", text: "温度降低达到饱和点" },
            { value: "C", text: "紫外线作用" },
            { value: "D", text: "风速增大" }
          ]
        },
        {
          text: "积雨云的形成过程是：",
          options: [
            { value: "A", text: "小水滴碰撞聚合" },
            { value: "B", text: "冰晶直接堆积" },
            { value: "C", text: "气压突变导致" },
            { value: "D", text: "温度骤降形成" }
          ]
        },
        {
          text: "云中电荷产生的机制是：",
          options: [
            { value: "A", text: "冰晶相互碰撞摩擦" },
            { value: "B", text: "温度梯度作用" },
            { value: "C", text: "重力分离效应" },
            { value: "D", text: "磁场感应作用" }
          ]
        },
        {
          text: "云层电荷分布的特点是：",
          options: [
            { value: "A", text: "顶部负电荷，底部正电荷" },
            { value: "B", text: "顶部正电荷，底部负电荷" },
            { value: "C", text: "电荷均匀分布" },
            { value: "D", text: "随机分布" }
          ]
        },
        {
          text: "空气被击穿的条件是：",
          options: [
            { value: "A", text: "温度超过100°C" },
            { value: "B", text: "电场强度超过阈值" },
            { value: "C", text: "湿度达到100%" },
            { value: "D", text: "气压降到最低" }
          ]
        },
        {
          text: "闪电放电的本质是：",
          options: [
            { value: "A", text: "空气分子燃烧" },
            { value: "B", text: "电荷快速中和" },
            { value: "C", text: "磁场突然变化" },
            { value: "D", text: "重力场扭曲" }
          ]
        },
        // 应用理解 9-10
        {
          text: "如果没有温度梯度，闪电还能形成吗？为什么？",
          options: [
            { value: "A", text: "能，因为电荷分离不依赖温度" },
            { value: "B", text: "不能，因为没有上升气流" },
            { value: "C", text: "能，风力可以替代" },
            { value: "D", text: "不确定" }
          ]
        },
        {
          text: "为什么沙漠地区很少发生雷暴？",
          options: [
            { value: "A", text: "沙漠没有水汽" },
            { value: "B", text: "温差不够大" },
            { value: "C", text: "缺乏对流条件" },
            { value: "D", text: "电阻率太高" }
          ]
        },
        // 知识迁移 11-12
        {
          text: "基于闪电形成原理，高楼更容易被雷击的原因是：",
          options: [
            { value: "A", text: "高楼材料导电性好" },
            { value: "B", text: "高楼提供了更短的放电路径" },
            { value: "C", text: "高楼产生电磁场" },
            { value: "D", text: "高楼改变气流方向" }
          ]
        },
        {
          text: "人工引发闪电现象的可能方法是：",
          options: [
            { value: "A", text: "增加空气湿度" },
            { value: "B", text: "用火箭拖拽导线到云中" },
            { value: "C", text: "发射激光束" },
            { value: "D", text: "释放带电粒子" }
          ]
        }
      ],
      knowledgeAnswers: Array(12).fill(null),

      // step 5: 认知负荷量表
      cogQuestions: [
        { text: "心理需求：这个学习任务在心理和感知活动方面的要求程度如何？" },
        { text: "努力程度：为了达到表现水平，您需要多努力地工作？" },
        { text: "挫折程度：在任务执行过程中，您感到多不安全、沮丧、烦躁？" },
      ],
      cogAnswers: Array(3).fill(null),

      // 使用意愿与体验评估
      systemQuestions: [
        { text: "如果有机会，我愿意继续使用这个AI学习系统" },
        { text: "我会向同学推荐这个AI学习系统" },
        { text: "我希望学校采用类似的AI教学系统" },
        { text: "我对这次的AI学习体验感到满意" },
        { text: "这个AI系统帮助我有效学习了闪电知识" },
        { text: "我觉得用AI学习比传统方式更有趣" },
      ],
      systemAnswers: Array(6).fill(null),
      
      // 系统体验量表与开放题
      socialQuestions: [
        { text: "我感觉AI助手就在我身边" },
        { text: "AI助手似乎意识到我的存在" },
        { text: "我觉得我和AI助手在同一个空间中" },
        { text: "AI助手的反应让我觉得它能感知到我" },
        { text: "我感觉与AI助手有真实的连接" },
        { text: "交互过程中我感受到了社交的氛围" },
      ],
      socialAnswers: Array(6).fill(null),

      // 系统体验量表与开放题
      techQuestions: [
        { text: "我相信这个AI助手是可靠的" },
        { text: "我相信这个AI助手会按预期工作" },
        { text: "我信任这个AI助手的功能" },
        { text: "总的来说，这个AI助手是值得信赖的" },
        { text: "我相信这个AI助手会保护我的学习利益" },
      ],
      techAnswers: Array(5).fill(null),
      errorMessage: '',
    };
  },
  created() {
    this.$cookies.set('flowState', 'postTest');
    this.$nextTick(() => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });

  },
  methods: {
    handleAffectSubmit () {
      checkFillStep(this, this.affectAnswers)
    },
    handleSubjectiveSubmit() {
      checkFillStep(this, this.subjectiveAnswers)
    },
    handleGodSubmit() {
      checkFillStep(this, this.godAnswers)
    },
    handleKnowledgeSubmit() {
      checkFillStep(this, this.knowledgeAnswers)
    },
    handleCogSubmit() {
      checkFillStep(this, this.cogAnswers)
    },
    handleSystemSubmit() {
      checkFillStep(this, this.systemAnswers)
    },
    handleSocialSubmit (){
      checkFillStep(this, this.socialAnswers)
    },
    handleTechSubmit () {
      if (checkFill(this, this.techAnswers)) this.submitAllQuestionnaireData();
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
      
      const affectPayload = {
        questions: this.affectQuestions,
        answers: this.affectAnswers,
        positive: this.affectAnswers.slice(0, 4).reduce((sum, val) => sum + val, 0) / this.affectAnswers.length * 2,
        negative: this.affectAnswers.slice(4, 8).reduce((sum, val) => sum + val, 0) / this.affectAnswers.length * 2,
      }
      const subjectivePayload = {
        questions: this.subjectiveQuestions,
        answers: this.subjectiveAnswers,
      }
      
      const godPayload = {
        questions: this.godQuestions,
        answers: this.godAnswers,
        anthropomorphism: this.godAnswers.slice(0, 2).reduce((sum, val) => sum + val, 0) / 2,
        animacy: this.godAnswers.slice(2, 4).reduce((sum, val) => sum + val, 0) / 2,
        likeability: this.godAnswers.slice(4, 6).reduce((sum, val) => sum + val, 0) / 2,
        godspeed: this.godAnswers.slice(0, 6).reduce((sum, val) => sum + val, 0) / 6,
      }
              
      // 计分
      const correct = ["B", "B", "B", "A", "A", "B", "B", "B", "B", "C", "B", "B"];
      let concept = 0, application = 0, transfer = 0;
      for (let i = 0; i < 8; i++) if (this.knowledgeAnswers[i] === correct[i]) concept++;
      for (let i = 8; i < 10; i++) if (this.knowledgeAnswers[i] === correct[i]) application++;
      for (let i = 10; i < 12; i++) if (this.knowledgeAnswers[i] === correct[i]) transfer++;
      const knowledgeScore = concept + application + transfer;
      const knowledgePayload = {
        questions: this.knowledgeQuestions,
        answers: this.knowledgeAnswers,
        conceptScore: concept,
        applicationScore: application,
        transferScore: transfer,
        knowledgeScore: knowledgeScore,
      };

      const cogPayload = {
        questions: this.cogQuestions,
        answers: this.cogAnswers,
        cogLoad: this.cogAnswers.reduce((sum, val) => sum + val, 0) / this.cogAnswers.length,
      }

      const systemPayload = {
        questions: this.systemQuestions,
        answers: this.systemAnswers,
        // 计算继续使用意愿、学习满意度、系统易用性分数
        willingness: this.systemAnswers.slice(0, 3).reduce((sum, val) => sum + val, 0) / this.systemAnswers.length * 2,
        satisfaction: this.systemAnswers.slice(3, 6).reduce((sum, val) => sum + val, 0) / this.systemAnswers.length * 2,
      }

      const socialPayload = {
        questions: this.socialQuestions,
        answers: this.socialAnswers,
        socialPresence: this.socialAnswers.reduce((sum, val) => sum + val, 0) / this.socialAnswers.length
      }

      const techPayload = {
        questions: this.techQuestions,
        answers: this.techAnswers,
        techTrust: this.techAnswers.reduce((sum, val) => sum + val, 0) / this.techAnswers.length
      }

      const payload = {
        userId: this.$store.state.userInfo?.userId || '',
        userName: this.$store.state.userInfo?.userName || '',
        time,
        affect: affectPayload,
        subjective: subjectivePayload,
        godSpeed: godPayload,
        knowledge: knowledgePayload,
        cognitive: cogPayload,
        system: systemPayload,
        social: socialPayload,
        technical: techPayload,
      }

      this.$ws.send(JSON.stringify({
        type: 'post_questionnaire',
        data: payload
      }))
      this.$store.commit('setStateToNext', { currentState: this.$store.state.flowState, delay: 0 });
    },
    showError(msg) {
      this.errorMessage = msg;
    },
  },
};
</script>
