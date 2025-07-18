<template>
  <div>
    <InfoRead v-if="flowState === flowStateEnum.readInfo" />
    <InfoCollect v-if="flowState === flowStateEnum.collectInfo" />
    <AiChat v-if="flowState === flowStateEnum.AIchat" />
    <PostQuestionnaire v-if="flowState === flowStateEnum.postTest" />
    <AllEnd v-if="flowState === flowStateEnum.end" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import InfoRead from './components/InfoRead.vue'
import InfoCollect from '@/components/InfoCollect.vue'
import AiChat from '@/components/AIChat.vue'
import PostQuestionnaire from './components/PostQuestionnaire.vue'
import AllEnd from './components/AllEnd.vue'

export default {
  name: 'App',
  components: { InfoRead, InfoCollect, AiChat, PostQuestionnaire, AllEnd },
  computed: {
    ...mapState(['flowState', 'flowStateEnum'])
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
  margin-top: 60px;
}
</style>
