<template>
  <div class="container">
    <a-button type="primary" @click="$router.push('/home')">回到主页</a-button>
    <h1>Task Results</h1>
    <a-radio-group class="tabs" v-model="activeName" @change="(e) => handleTabClick(e.target.value)">
      <a-radio-button v-for="tab in tabs" :key="tab.key" :value="tab.key">{{tab.title}}</a-radio-button>
    </a-radio-group>
    <div class="image-container">
      <img v-if="images['wordcloud'] && visibleTabs['wordcloud']" class="image" :src="images['wordcloud']" alt="词云">
    </div>
  </div>
</template>
<script>
import axiosInstance from "@/api/axiosInstance";
import { message } from "ant-design-vue";
import { ref } from "vue";

export default {
  name: "JdComment",
  setup() {
    return {
      activeName: ref('wordcloud'),
    };
  },
  data() {
    return {
      images: {},
      tabs: [
        { key: 'wordcloud', title: '词云' },
      ],
      visibleTabs: {
        wordcloud: false,
      }
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
  mounted() {
    this.taskId = this.$route.params.taskId;
    console.log(this.taskId)
  }
}
</script>

<style scoped>
.container {
  max-width: 960px;
  margin: 0 auto;
  padding: 1rem;
  text-align: center;
}

.tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

.image-container {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.image {
  max-width: 100%;
  margin: 1rem;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
}
</style>