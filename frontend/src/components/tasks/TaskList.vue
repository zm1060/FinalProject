<template>
  <div>
    <a-card title="Task Counter">
      <a-row>
        <a-col v-for="(count, taskType) in taskCounts" :key="taskType" :span="6">
          <div class="counter" @click="showTasks(taskType)">
            <div>{{ taskType }}</div>
            <div>{{ count }}</div>
          </div>
        </a-col>
      </a-row>
    </a-card>

    <a-table :columns="taskColumns" :dataSource="tasks" v-if="showTaskTable">
    </a-table>

    <a-table :columns="dataColumns" :dataSource="data" v-if="showDataTable">
    </a-table>

    <div ref="chart" style="height: 300px;"></div>
  </div>
</template>

<script>
import axios from 'axios';
import echarts from 'echarts';
import { Card, Row, Col, Table } from 'ant-design-vue';

export default {
  name: 'TaskList',
  components: {
    'a-card': Card,
    'a-row': Row,
    'a-col': Col,
    'a-table': Table,
  },
  data() {
    return {
      taskCounts: {},
      tasks: [],
      data: [],
      taskColumns: [
        // Define your columns for task table
      ],
      dataColumns: [
        // Define your columns for data table
      ],
      showTaskTable: false,
      showDataTable: false,
    };
  },
  created() {
    this.fetchTaskCounts();
    this.fetchTasks();
  },
  methods: {
    fetchTaskCounts() {
      axios.get('/user/tasks').then(response => {
        this.taskCounts = response.data.length();
        this.renderChart();
      });
    },
    renderChart() {
      const chart = echarts.init(this.$refs.chart);
      chart.setOption({
        // Define your chart options and data
      });
      chart.on('click', params => {
        this.showTasks(params.name);
      });
    },
    fetchTasks() {
      axios.get('/tasks').then(response => {
        this.tasks = response.data;
      });
    },
    showTasks(taskType) {
      this.showTaskTable = true;
      axios.get(`/tasks?type=${taskType}`).then(response => {
        this.tasks = response.data;
      });
    },
    showData(taskId) {
      this.showDataTable = true;
      axios.get(`/tasks/${taskId}/data`).then(response => {
        this.data = response.data;
      });
    },
  },
};
</script>
