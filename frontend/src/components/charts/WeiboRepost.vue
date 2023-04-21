<template>
  <div class="container">
    <a-button type="primary" @click="$router.push('/home')">回到主页</a-button>
    <h1>Task Results</h1>
    <a-layout>
      <a-layout-sider :width="200">
        <a-radio-group class="tabs" v-model="activeName" @change="(e) => handleTabClick(e.target.value)">
          <a-radio-button v-for="tab in tabs" :key="tab.key" :value="tab.key">{{tab.title}}</a-radio-button>
        </a-radio-group>
      </a-layout-sider>
      <a-layout-content>
        <div class="image-container">
          <div v-for="tab in visibleImageTabs" :key="tab.key" class="image">
            <img :src="images[tab.key]" :alt="tab.title" />
            <div class="image-label">{{ tab.title }}</div>
          </div>
        </div>
      </a-layout-content>
    </a-layout>
  </div>
</template>

<script>
import axiosInstance from "@/api/axiosInstance";
import { message } from "ant-design-vue";
import { ref } from "vue";

export default {
  name: "WeiboRepost",
  setup() {
    return {
      activeName: ref('post_sources'),
    };
  },
  computed: {
    visibleImageTabs() {
      return this.tabs.filter(tab => this.visibleTabs[tab.key]);
    }
  },
  data() {
    return {
      images: {},
      tabs: [
        { key: 'post_sources', title: '博文的发布设备分布' },
        { key: 'sentiment_histogram', title: '博文的情感分布' },
        { key: 'posting_frequency', title: '博文发布频率' },
        { key: 'user_engagement', title: '博文用户参与度' },
        { key: 'top_hashtags', title: '前十标签' },
      ],
      visibleTabs: {
        post_sources: false,
        sentiment_histogram: false,
        posting_frequency: false,
        user_engagement: false,
        top_hashtags: false,
      },
    }
  },
  methods: {
    async handleTabClick(tabKey) {
      this.taskId = this.$route.params.taskId;
      this.visibleTabs[tabKey] = !this.visibleTabs[tabKey]
      if (!this.images[tabKey]) {
        // Get the image data for the selected tab
        axiosInstance.get(`/analyze/result/${this.taskId}/${tabKey}`, {
          responseType: 'arraybuffer',
          headers: {'Accept': 'image/png'}
        })
          .then(response => {
            // Convert the ArrayBuffer to a base64 string
            const base64 = btoa(
              new Uint8Array(response.data).reduce(
                (data, byte) => data + String.fromCharCode(byte),
                '',
              ),
            );
            // Set the image data for the selected tab
            this.images[tabKey] =   `data:image/png;base64,${base64}`
            message.success('加载成功',0.2)
          })
          .catch(error => {
            console.error(error);
          });
      }
    }
  },
  async mounted() {
    this.taskId = this.$route.params.taskId;
  }
}
</script>
<style scoped>
.ant-layout-sider {
    position: relative;
    min-width: 0;
    background: #ffffff;
    transition: all 0.2s;
}
</style>