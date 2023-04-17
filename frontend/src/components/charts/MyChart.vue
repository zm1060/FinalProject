<template>
  <div>
    <v-chart :options="chartOptions"></v-chart>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import VChart from 'vue-echarts'
import axios from 'axios'

export default defineComponent({
  name: 'MyChart',
  components: {
    VChart
  },
  props: {
    taskId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      chartOptions: {}
    }
  },
  async mounted() {
    // 向后端API发送请求，获取与任务ID关联的图表数据
    const response = await axios.get(`/api/get_chart?task_id=${this.taskId}`)
    // 将图表数据保存为图表选项对象，并传递给Vue图表组件
    this.chartOptions = {
      series: [{
        type: 'line',
        data: response.data.chartData
      }]
    }
  }
})
</script>
