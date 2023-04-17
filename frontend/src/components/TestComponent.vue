<template>
  <div>
    <my-chart :task-id="taskId"></my-chart>
  </div>
</template>

<script>

import MyChart from "@/components/charts/MyChart.vue";

export default {
  components: {
    MyChart
  },
  data() {
    return {
      taskId: '12345'
    }
  }
}
</script>
