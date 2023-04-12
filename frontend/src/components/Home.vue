<template>
  <div class="container">
    <div class="header">
      <h1>欢迎使用!</h1>
      <nav>
        <ul>
          <li><router-link to="/user_center">用户中心</router-link></li>
          <li><router-link to="/task_center">任务中心</router-link></li>
          <li><router-link to="/weibo/run_tasks">微博爬虫</router-link></li>
          <li><router-link to="/jd/run_tasks">京东爬虫</router-link></li>
          <li><router-link to="/data_analysis">数据分析</router-link></li>
          <li><router-link to="/data_management">数据管理</router-link></li>
        </ul>
      </nav>
    </div>

    <div class="content">
      <div class="profile">
        <div class="avatar">
          <img src="/img/avatar.jpg" alt="User Avatar">
        </div>
        <div class="info">
          <h2>{{ currentUser.name }}</h2>
          <a class="link" href="mailto:{{ currentUser.email }}">{{ currentUser.email }}</a>
          <br>
          <a class="button" href="#">Edit Profile</a>
        </div>
      </div>

      <div class="stats">
        <div class="stat">
          <h3 class="stat_completed">Tasks Completed</h3>
          <p class="stat_completed">{{ taskCounts.completed }}</p>
        </div>
        <div class="stat">
          <h3 class="stat_failed">Tasks Failed</h3>
          <p class="stat_failed">{{ taskCounts.failed }}</p>
        </div>
        <div class="stat">
          <h3 class="stat_running">Tasks Running</h3>
          <p class="stat_running">{{ taskCounts.running }}</p>
        </div>
      </div>

      <div class="visualization">
        <h2>Data Visualization</h2>
        <div class="chart">
          <echarts :options="chartOptions"></echarts>
        </div>
      </div>

      <div class="table">
        <h2>Task List</h2>
        <a-table :columns="columns" :data-source="tasks">
        </a-table>
      </div>
    </div>
  </div>
</template>

<script>
import { Table } from 'ant-design-vue';
import axiosInstance from "@/api/axiosInstance";

export default {
  name: 'HomePage',
  components: {
    'a-table': Table,
  },
  data() {
      return {
          currentUser: {
              name: 'Ming Zuo',
              email: 'zm1575098153@gmail.com',
          },
          taskCounts: {
              completed: 10,
              failed: 2,
              running: 4,
          },
          chartOptions: {
              // Define your chart options and data
          },
          columns: [
              // Define your columns for the task table
          ],
          tasks: [
              // Define your tasks data here
          ],
      };
  },
  methods: {
      fetchTasks()
      {
          axiosInstance.get('/user/tasks').then(response => {
              const tasks = response.data;
              const columns = [
                  // Define your columns for the task table
              ];
              this.tasks = tasks.map(task => ({
                  ...task,
                  key: task.task_id,
              }));
              this.columns = columns;
          });
      },

  },
  mounted()
  {
      this.fetchTasks();
  }
};
</script>


<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 50px 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 50px;
}

.header h1 {
  font-size: 36px;
  font-weight: bold;
}

.header nav ul {
  list-style-type: none;
  display: flex;
}

.header nav li {
  margin: 0 10px;
}

.header nav a {
  font-size: 24px;
  color: #333;
}

.profile {
  display: flex;
  align-items: center;
  margin-bottom: 50px;
  color: blue;
}

.avatar {
  width: 100px;
  height: 100px;
  margin-right: 20px;
  overflow: hidden;
  border-radius: 50%;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.info h2 {
  font-size: 32px;
  margin-bottom: 10px;
}

.info p {
  font-size: 24px;
  margin-bottom: 20px;
}

.link{
  font-size: 24px;
  margin-bottom: 20px;
}

.button {
  display: inline-block;
  padding: 10px 20px;
  font-size: 24px;
  font-weight: bold;
  text-transform: uppercase;
  background-color: #333;
  color: #fff;
  border-radius: 5px;
  text-decoration: none;
}

.stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 50px;
}

.stat {
  flex-basis: 30%;
  text-align: center;
}

.stat_completed{
  flex-basis: 30%;
  text-align: center;
  color: limegreen;
}

.stat_failed{
  flex-basis: 30%;
  text-align: center;
  color: crimson;
}

.stat_running{
  flex-basis: 30%;
  text-align: center;
  color: darkorange;
}
.stat h3 {
  font-size: 24px;
  margin-bottom: 10px;
}

.stat p {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 10px;
}

.visualization h2 {
  font-size: 32px;
  margin-bottom: 20px;
}

.chart {
  height: 500px;
}

.table h2 {
  font-size: 32px;
  margin-bottom: 20px;
}

.ant-table-wrapper {
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.ant-table-thead > tr > th {
  background-color: #f2f2f2;
  font-weight: bold;
  font-size: 18px;
}

.ant-table-tbody > tr > td {
  font-size: 16px;
}
</style>