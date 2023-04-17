<template>
    <div>
    <a-layout style="min-height: 10vh">
      <a-menu mode="horizontal" theme="dark">
        <a-menu-item>
          <router-link to="/home">基于NLP的可视化评价信息收集与分析系统</router-link>
        </a-menu-item>
        <a-menu-item>
          <router-link to="/user_center">用户中心</router-link>
        </a-menu-item>
        <a-menu-item>
          <router-link to="/task_center">任务中心</router-link>
        </a-menu-item>
        <a-sub-menu title="爬虫">
          <a-menu-item>
            <router-link to="/weibo/run_tasks">微博爬虫</router-link>
          </a-menu-item>
          <a-menu-item>
            <router-link to="/jd/run_tasks">京东爬虫</router-link>
          </a-menu-item>
        </a-sub-menu>
        <a-menu-item>
          <router-link to="/data_analysis">数据分析</router-link>
        </a-menu-item>
        <a-menu-item>
          <router-link to="/data_management">数据管理</router-link>
        </a-menu-item>
        <a-menu-item>
          <router-link to="/user_center">{{currentUser.username}}</router-link>
        </a-menu-item>
        <a-menu-item>
          <a class="link" href="mailto:{{ currentUser.email }}">{{ currentUser.email }}</a>
        </a-menu-item>
        <a-menu-item>
          <a class="button" href="#">退出登录</a>
        </a-menu-item>
      </a-menu>

      <a-layout-content style="padding: 0 50px">
<!--        <div class="stats">-->
<!--          <div class="stat">-->
<!--            <h3 class="stat_completed">Tasks Completed</h3>-->
<!--            <p class="stat_completed">{{ taskCounts.completed }}</p>-->
<!--          </div>-->
<!--          <div class="stat">-->
<!--            <h3 class="stat_failed">Tasks Failed</h3>-->
<!--            <p class="stat_failed">{{ taskCounts.failed }}</p>-->
<!--          </div>-->
<!--          <div class="stat">-->
<!--            <h3 class="stat_running">Tasks Running</h3>-->
<!--            <p class="stat_running">{{ taskCounts.running }}</p>-->
<!--          </div>-->
<!--        </div>-->

        <div class="visualization">
          <h2>Data Visualization</h2>
          <div class="chart">
            <v-chart ref="myChart" :option="chartOptions" autoresize></v-chart>
          </div>
        </div>

        <div class="table">
          <h2>任务列表</h2>
          <a-table :columns="columns" :data-source="tasks" :loading="loading">
            <template v-slot:action="{ record }">
              <span>
                <a-button type="primary" @click="handleView(record.task_id, record.task_type)">
                  查看
                </a-button>
                <a-button type="primary" @click="handleAnalyze(record.task_id)">分析</a-button>
                <a-popconfirm
                  title="Are you sure to delete this task?"
                  @confirm="handleDelete(record.task_id)"
                >
                  <a-button type="danger">删除</a-button>
                </a-popconfirm>
              </span>
            </template>
          </a-table>
        </div>

      </a-layout-content>
    </a-layout>
  </div>
</template>

<script>
import {message, Table} from 'ant-design-vue';
import axiosInstance from "@/api/axiosInstance";

import { GridComponent } from "echarts/components";
import ECharts from "vue-echarts";
import "echarts/lib/chart/bar";
import "echarts/lib/component/tooltip";
import "echarts/lib/component/title";
import "echarts/lib/component/legend";
import 'zrender/lib/canvas/canvas';
import {use} from "echarts";

use([GridComponent]); // Use GridComponent


export default {
  name: 'HomePage',
  components: {
    'a-table': Table,
    'v-chart': ECharts
  },
  data() {
      return {
          currentUser: {
              username: '',
              email: '',
          },
          taskCounts: {
              completed: 10,
              failed: 2,
              running: 4,
          },
          chartOptions: {

          },
          loading: false,
          columns: [
            {
              title: "任务ID",
              dataIndex: "task_id",
              key: "task_id",
            },
            {
              title: "任务种类",
              dataIndex: "task_type",
              key: "task_type",
            },
            {
              title: "开始时间",
              dataIndex: "task_time",
              key: "task_time",
            },
            {
              title: "完成时间",
              dataIndex: ["stats", "finish_time"],
              key: "finish_time",
            },
            {
              title: "爬取条目数量",
              dataIndex: ["stats", "item_scraped_count"],
              key: "item_scraped_count",
            },
            {
              title: "操作",
              key: "action",
              slots: { customRender: "action" },
            },
          ],
          tasks: [],
      };
  },


  methods: {
    setChartData() {
      const data = {};

      this.tasks.forEach(task => {
        if (data[task.task_type]) {
          data[task.task_type]++;
        } else {
          data[task.task_type] = 1;
        }
      });

      const xAxisData = Object.keys(data);
      const seriesData = xAxisData.map(key => data[key]);

      this.chartOptions.title = {
        text: '任务种类'
      };
      this.chartOptions.tooltip = {};
      this.chartOptions.legend = {
        data: ['Task Types']
      };
      this.chartOptions.xAxis = {
        type: 'category',
        data: xAxisData
      };
      this.chartOptions.yAxis = {
        type: 'value'
      };
      this.chartOptions.series = [{
        name: 'Task Types',
        type: 'bar',
        data: seriesData
      }];

      this.$nextTick(() => {
        this.$refs.myChart.resize();
      });
    },
    async fetchTasks() {
      this.loading = true;
      axiosInstance
        .get("/user/tasks")
        .then((response) => {
          this.tasks = response.data;
          this.setChartData(); // Call this method here
          message.success("加载任务列表成功!",0.3);
        })
        .catch((error) => {
          message.error("加载失败!(当前用户token过期)",1);
          console.log(error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    async getUserInfo() {
      try {
        const response = await axiosInstance.get('/me')
        this.currentUser.username = response.data.username
        this.currentUser.email = response.data.email
        message.success("加载用户信息成功!",0.2)
      } catch (error) {
        console.error(error)
        message.error("加载用户信息失败!请检查登录状态!",1)
      }
    },
    handleView(taskId, taskType) {
      const routeName = `${taskType}_list`;
      console.log('Generated route name:', routeName);

      // pass the taskId to the component as a route parameter
      this.$router
        .push(`/${routeName}/${taskId}`)
        .catch((error) => {
          console.error('Navigation failed:', error);
        });
    },
    handleDelete(taskId) {
      axiosInstance
        .delete(`/user/tasks/${taskId}`)
        .then((response) => {
          message.success("删除成功!");
          this.fetchTasks();
          console.log(response);
        })
        .catch((error) => {
          message.error("删除失败!");
          console.log(error);
        });
    },
    handleAnalyze(taskId){
      axiosInstance.get(`/weibo/analyze/${taskId}`)
          .then((response)=>{
            message.success("Success!");
            console.log(response);
          })
          .catch((error)=>{
              message.error("Error!");
              console.log(error);
          })

    },

  },
  mounted()
  {
      this.getUserInfo();
      this.fetchTasks();
  }
};
</script>

<style scoped>
  .avatar {
    width: 80px;
    height: 80px;
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
    font-size: 28px;
    margin-bottom: 10px;
    font-weight: bold;
  }

  .info p, .link{
    font-size: 16px;
    margin-bottom: 10px;
  }

  .link{
    display: block;
    color: #0072ff;
    text-decoration: none;
  }

  .button {
    display: inline-block;
    padding: 10px 20px;
    font-size: 16px;
    font-weight: bold;
    text-transform: uppercase;
    background-color: #333;
    color: #fff;
    border-radius: 5px;
    text-decoration: none;
    margin-top: 10px;
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
    font-size: 18px;
    margin-bottom: 10px;
    font-weight: bold;
  }

  .stat p {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 10px;
  }


  .visualization {
    margin-top: 30px;
  }

  .chart {
    width: 100%;
    height: 400px;
  }

  .table {
    margin-top: 30px;
  }

  .link {
    color: #1890ff;
    text-decoration: none;
  }

  .link:hover {
    text-decoration: underline;
  }

  .button {
    color: #1890ff;
    background-color: transparent;
    border: none;
    cursor: pointer;
    text-decoration: underline;
  }

  .button:focus {
    outline: none;
  }

  h2 {
    margin-bottom: 20px;
  }
</style>