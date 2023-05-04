<template>
  <div>
    <a-button type="primary" @click="$router.push('/home')">返回主页</a-button>
    <h1>任务列表</h1>
    <a-table :columns="columns" :data-source="tasks" :loading="loading">
      <template v-slot:[`status`]="{ text }">
        <a-badge :status="text === 'finished' ? 'success' : 'processing'">{{ text }}</a-badge>
      </template>
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
</template>

<script>
import { message, Table, Popconfirm, Button } from "ant-design-vue";
import axiosInstance from "@/api/axiosInstance";

export default {
  name: "MyTasks",
  components: {
    "a-table": Table,
    "a-popconfirm": Popconfirm,
    "a-button": Button,
  },
  data() {
    return {
      tasks: [],
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
    };
  },
  created() {
    this.fetchTasks();
  },
  methods: {
    fetchTasks() {
      this.loading = true;
      axiosInstance
        .get("/user/tasks")
        .then((response) => {
          this.tasks = response.data;
          console.log(this.tasks)
          message.success("加载任务列表成功!");
        })
        .catch((error) => {
          message.error("加载失败!(当前用户token过期)");
          console.log(error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    handleView(taskId, taskType) {
      const routeName = `${taskType}_list`;
      console.log('Generated route name:', routeName);

      // pass the taskId to the component as a route parameter
      this.$router.push(`/${routeName}/${taskId}`)
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
};
</script>
