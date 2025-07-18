<template>
  <div>
    <InfoCollect v-if="!infoCollectSubmitted" @submitted="infoCollectSubmitted = true" />
    <AiChat v-if="infoCollectSubmitted && !AIChatComplete" @chatComplete="AIChatComplete = true"/>
    <PostQuestionnaire v-if="AIChatComplete" />
  </div>
</template>

<script>
import AiChat from '@/components/AIChat.vue'
import InfoCollect from '@/components/InfoCollect.vue'
import PostQuestionnaire from './components/PostQuestionnaire.vue'

export default {
  name: 'App',
  components: { AiChat, InfoCollect, PostQuestionnaire},
 data() {
    return {
      infoCollectSubmitted: false,
      AIChatComplete: false
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
  margin-top: 60px;
}
</style>
