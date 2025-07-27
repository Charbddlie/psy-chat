<template>
  <div>
    <InfoRead v-if="flowState === flowStateEnum.readInfo" />
    <InfoCollect v-if="flowState === flowStateEnum.collectInfo" />
    <PreQuestionnaire v-if="flowState === flowStateEnum.preTest" />
    <AIChat v-if="flowState === flowStateEnum.AIChat" />
    <PostQuestionnaire v-if="flowState === flowStateEnum.postTest" />
    <AllEnd v-if="flowState === flowStateEnum.end" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import InfoRead from './pages/InfoRead.vue'
import InfoCollect from '@/pages/InfoCollect.vue'
import PreQuestionnaire from './pages/PreQuestionnaire.vue'
import AIChat from '@/pages/AIChat.vue'
import PostQuestionnaire from './pages/PostQuestionnaire.vue'
import AllEnd from './pages/AllEnd.vue'

export default {
  name: 'App',
  components: { InfoRead, InfoCollect, PreQuestionnaire, AIChat, PostQuestionnaire, AllEnd },
  computed: {
    ...mapState(['flowState', 'flowStateEnum'])
  },
  created() {
    const userId = this.$cookies.get('userId') || '';
    const userName = this.$cookies.get('userName') || '';
    const flowState = this.$cookies.get('flowState') || '';
    console.log('userId:', userId, 'userName:', userName, 'flowState:', flowState);
    if (!flowState || !userId || !userName) {
      return;
    } else {
      console.log('获取cookie成功, userId:', userId, 'userName:', userName, 'flowState:', flowState);
      this.$store.commit('setUserInfo', { userId: userId, userName: userName });
      this.$store.commit('setState', flowState);
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}

body {
  margin: 0 !important;
}
</style>
