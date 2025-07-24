<template>
  <div class="end-container">
    <div class="end-card">
      <h2>🎉实验已结束,感谢您的参与!🙏</h2>
      <div class="end-content">
        <p>
          您的问卷已成功提交。<br>
          <span class="emoji">🌟🌩️📚</span>
        </p>
        <div class="end-tip">
          祝您学习进步，生活愉快！
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AllEnd'
}
</script>

<style scoped>
.end-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
}
.end-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 6px 32px rgba(80, 120, 200, 0.12), 0 1.5px 6px rgba(0,0,0,0.04);
  padding: 38px 44px 32px 44px;
  max-width: 480px;
  width: 100%;
  text-align: center;
  animation: fadeIn 0.8s;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(30px);}
  to { opacity: 1; transform: translateY(0);}
}
.end-card h2 {
  color: #10b981;
  margin-bottom: 18px;
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: 1px;
}
.end-content {
  font-size: 1.13rem;
  color: #333;
  margin-bottom: 24px;
  text-align: center;
}
.emoji {
  font-size: 1.5rem;
  display: block;
  margin: 16px 0 0 0;
}
.end-tip {
  margin: 18px 0 0 0;
  font-size: 1.1rem;
  color: #6366f1;
  font-weight: 600;
  text-align: center;
  letter-spacing: 1px;
}
</style>