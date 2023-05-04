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
          <router-link to="/help_center">帮助中心</router-link>
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
                <a-button type="primary" @click="handleAnalyze(record.task_id, record.task_type)">分析</a-button>
                <a-button type="primary" @click="handleResult(record.task_id, record.task_type)">查看分析结果</a-button>
                <a-popconfirm
                  title="是否确定删除这个任务?"
                  @confirm="handleDelete(record.task_id)"
                >
                  <a-button type="danger">删除</a-button>
                </a-popconfirm>
                <a-button
                  v-if="!isRunning(record)"
                  type="primary"
                  @click="handleRestart(record.task_id, record.task_type)"
                >
                  恢复
                </a-button>
                <a-popconfirm
                  v-if="isRunning(record)"
                  title="是否确定停止这个任务?"
                  @confirm="handleStop(record.task_id, record.task_type)"
                >
                  <a-button type="danger">停止</a-button>
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
              sorter: (a, b) => new Date(a.task_time) - new Date(b.task_time),
            },
            {
              title: "完成时间",
              dataIndex: ["stats", "finish_time"],
              key: "finish_time",
              sorter: (a, b) => new Date(a.stats.finish_time) - new Date(b.stats.finish_time),
            },
            {
              title: "爬取条目数量",
              dataIndex: ["stats", "item_scraped_count"],
              key: "item_scraped_count",
              sorter: (a, b) => a.stats.item_scraped_count - b.stats.item_scraped_count,
            },
            {
              title: '状态',
              dataIndex: "status",
              key: 'status',
              sorter: (a, b) => a.status.localeCompare(b.status),
            },
            {
              title: "操作",
              key: "action",
              slots: { customRender: "action" },
            },
          ],
          isRunning: (record) => {
            return record.status === 'running';
          },
          modalVisible: false,
          selectedTaskId: null,
          selectedTaskType: null,
          tasks: [],
      };
  },


  methods: {
      setChartData() {
      const data = {};
      const colors = {
        running: '#1890ff',
        finished: '#52c41a',
        stopped: '#ff4d4f',
      };

      // 根据任务类型和状态统计数据
      this.tasks.forEach(task => {
        if (data[task.task_type]) {
          if (data[task.task_type][task.status]) {
            data[task.task_type][task.status]++;
          } else {
            data[task.task_type][task.status] = 1;
          }
        } else {
          data[task.task_type] = {};
          data[task.task_type][task.status] = 1;
        }
      });

      const xAxisData = Object.keys(data);
      const legendData = Object.keys(colors);
      const seriesData = legendData.map((status) => ({
        name: status,
        type: 'bar',
        stack: 'task_type',
        data: xAxisData.map(task_type => data[task_type][status] || 0),
        itemStyle: {
          color: colors[status],
        },
        emphasis: {
          focus: 'series',
          itemStyle: {
            opacity: 1,
          },
        },
      }));

      this.chartOptions.title = {
        text: '任务种类和状态'
      };
      this.chartOptions.tooltip = {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow',
        },
      };
      this.chartOptions.legend = {
        data: legendData,
      };
      this.chartOptions.xAxis = {
        type: 'category',
        data: xAxisData,
      };
      this.chartOptions.yAxis = {
        type: 'value',
      };
      this.chartOptions.series = seriesData;

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
          message.error("加载失败!(当前用户token过期)",0.5);
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
        message.error("加载用户信息失败!请检查登录状态!",0.5)
      }
    },
    handleView(taskId, taskType) {
      const routeName = `${taskType}_list`;
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
    handleAnalyze(taskId, taskType) {
      let endpoint = '';
      switch (taskType) {
        case 'weibo_comment':
          endpoint = `/analyze/weibo/comment/${taskId}`;
          break;
        case 'weibo_tweet':
          endpoint = `/analyze/weibo/tweet/${taskId}`;
          break;
        case 'weibo_repost':
          endpoint = `/analyze/weibo/repost/${taskId}`;
          break;
        case 'weibo_search':
          endpoint = `/analyze/weibo/search/${taskId}`;
          break;
        case 'weibo_fan':
          endpoint = `/analyze/weibo/fan/${taskId}`;
          break;
        case 'weibo_follower':
          endpoint = `/analyze/weibo/follower/${taskId}`;
          break;
        case 'weibo_user':
          endpoint = `/analyze/weibo/user/${taskId}`;
          break;
        case 'jd_comment':
          endpoint = `/analyze/jd/comment/${taskId}`;
          break;
        case 'jd_product':
          endpoint = `/analyze/jd/product/${taskId}`;
          break;
        default:
          console.error('Invalid task type');
          return;
      }

      axiosInstance.post(endpoint)
        .then((response) => {
          message.success("Success!");
          console.log(response);
        })
        .catch((error) => {
          message.error("Error!");
          console.log(error);
        });
    },
    handleResult(taskId, taskType) {
      // Generate the route name based on the task type
      const routeName = `${taskType}_result`;

      // Navigate to the task result page with the task ID as a parameter
      this.$router.push({ name: routeName, params: { taskId } })
        .catch((error) => {
          console.error('Navigation failed:', error);
        });
    },
    handleStop(taskId, taskType) {
      let apiendpoint = "";
      if(taskType.startsWith("weibo_")){
          apiendpoint = `/weibo/stop_spider/${taskId}`
      }else if(taskType.startsWith("jd_")){
          apiendpoint = `/jd/stop_spider/${taskId}`
      }
      axiosInstance
        .get(apiendpoint)
        .then((response) => {
          message.success("任务已停止!");
          console.log(response);
          this.fetchTasks();
        })
        .catch((error) => {
          message.error("任务停止失败!");
          console.log(error);
        });
    },
    handleRestart(taskId, taskType) {
      let apiendpoint = "";
      if(taskType.startsWith("weibo_")){
          apiendpoint = `/weibo/resume_spider/${taskId}`
      }else if(taskType.startsWith("jd_")){
          apiendpoint = `/jd/resume_spider/${taskId}`
      }
      axiosInstance
        .get(apiendpoint)
        .then((response) => {
          message.success("任务已恢复!");
          console.log(response);
          this.fetchTasks();
        })
        .catch((error) => {
          message.error("任务恢复失败!");
          console.log(error);
        });
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