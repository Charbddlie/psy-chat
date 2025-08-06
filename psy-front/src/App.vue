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
    // 会在刚开始和info collect之后用到，只创建一次
    this.$ws.addMessageListener(this.handleChatCreatedMessage);

    const chat_id = this.$cookies.get('chat_id') || '';
    const user_id = this.$cookies.get('user_id') || '';
    const user_name = this.$cookies.get('user_name') || '';
    console.log('user_id:', user_id, 'user_name:', user_name);
    if (!chat_id || !user_id || !user_name) return;
    console.log('获取cookie成功, chat_id:', chat_id, 'user_id:', user_id, 'user_name:', user_name);
    
    this.$ws.send(JSON.stringify({
      type: 'chat_create',
      chat_id: chat_id,
      user_id: user_id,
      user_name: user_name,
    }));
  },
  methods: {
    handleChatCreatedMessage (response) {
      if (response.type == 'chat_created'){
        let added = false;
        console.log("chat_created")
        this.$ws.removeMessageListener(this.handleChatCreatedMessage);
        
        this.$store.commit('setChatId', response.chat_id);
        this.$store.commit('setUserInfo', { user_id: response.record.user_id, user_name: response.record.user_name });
        this.$store.commit('setHasHistory', (response.record.chat && !response.record.chat_complete));
        this.$cookies.set('user_id', response.record.user_id);
        this.$cookies.set('user_name', response.record.user_name);
        console.log('chat_id', response.chat_id)
        this.$cookies.set('chat_id', response.chat_id);
        // console.log(this.$store.state.chat_id)
        // console.log('setskip')

        added = false;
        if (response.record.info) {
          this.$store.commit('addSkipState', this.$store.state.flowStateEnum.collectInfo);
          added = true;
        }
        if (response.record.pre) {
          this.$store.commit('addSkipState', this.$store.state.flowStateEnum.preTest);
          added = true;
        }
        if (response.record.post) {
          this.$store.commit('addSkipState', this.$store.state.flowStateEnum.postTest);
          added = true;
        }
        if (response.record.chat_complete) {
          this.$store.commit('addSkipState', this.$store.state.flowStateEnum.AIChat);
          added = true;
        }
        // 只要有任何一个被添加，readInfo也要添加
        if (added) {
          this.$store.commit('addSkipState', this.$store.state.flowStateEnum.readInfo);
        }
      }
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
