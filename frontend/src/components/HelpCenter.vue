<template>
  <div class="help-center">
    <h1>帮助中心</h1>
    <p>Welcome to our Help Center! Here you can find information on how to use our system and get the most out of it. Below you will find a list of topics that we cover in our guide:</p>
    <ul>
      <li>Getting started</li>
      <li>Creating an account</li>
      <li>Navigation</li>
      <li>Features and tools</li>
      <li>Troubleshooting</li>
    </ul>
    <p>如果需要的话，可以点击下方按钮下载PDF版本的使用手册。</p>
    <a-button type="primary" @click="downloadGuide">下载</a-button>
    <p>If you have any questions or need further assistance, please <a href="mailto:248334369@qq.com">联系我</a>.</p>
    <div class="github-link">
      <a href="https://github.com/your-username/your-repo">GitHub</a>
      <a-button type="dashed" shape="circle" icon="github" href="https://github.com/your-username/your-repo"></a-button>
    </div>
  </div>
</template>
<script>
import { Button } from 'ant-design-vue';

export default {
  name: "HelpCenter",
  components: {
    'a-button': Button
  },
  methods: {
    downloadGuide() {
      // Add logic for downloading the guide here
    }
  }
}
</script>


<style scoped>
.help-center {
  max-width: 600px;
  margin: 0 auto;
  padding: 24px;
  border: 1px solid #d9d9d9;
  border-radius: 2px;
  background-color: #fff;
}

h1 {
  font-size: 32px;
  margin-bottom: 24px;
}

ul {
  margin-bottom: 24px;
}

li {
  font-size: 18px;
  margin-bottom: 8px;
}

p {
  font-size: 16px;
  margin-bottom: 16px;
}

.github-link {
  display: flex;
  align-items: center;
  margin-top: 24px;
}

.github-link a {
  margin-right: 8px;
}

a-button {
  margin-right: 8px;
}
</style>