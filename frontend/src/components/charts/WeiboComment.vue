<template>
  <div class="container">
    <a-button type="primary" @click="$router.push('/home')">回到主页</a-button>
    <h1>Task Results</h1>
    <a-radio-group class="tabs" v-model="activeName" @change="(e) => handleTabClick(e.target.value)">
      <a-radio-button v-for="tab in tabs" :key="tab.key" :value="tab.key">{{tab.title}}</a-radio-button>
    </a-radio-group>
    <div class="image-container">
      <img v-if="images['line_chart'] && visibleTabs['line_chart']" class="image" :src="images['line_chart']" alt="Line Chart">
      <img v-if="images['bar_chart'] && visibleTabs['bar_chart']" class="image" :src="images['bar_chart']" alt="Bar Chart">
      <img v-if="images['wordcloud'] && visibleTabs['wordcloud']" class="image" :src="images['wordcloud']" alt="WordCloud">
      <img v-if="images['heatmap'] && visibleTabs['heatmap']" class="image" :src="images['heatmap']" alt="HeatMap">
    </div>
  </div>
</template>
<script>
import axiosInstance from "@/api/axiosInstance";
import { message } from "ant-design-vue";
import { ref } from "vue";

export default {
  name: "WeiboComment",
  setup() {
    return {
      activeName: ref('line_chart'),
    };
  },
  data() {
    return {
      images: {},
      tabs: [
        { key: 'line_chart', title: 'Line Chart' },
        { key: 'bar_chart', title: 'Bar Chart' },
        { key: 'wordcloud', title: 'Word Cloud' },
        { key: 'heatmap', title: 'Heat Map' },
      ],
      visibleTabs: {
        line_chart: false,
        bar_chart: false,
        wordcloud: false,
        heatmap: false,
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