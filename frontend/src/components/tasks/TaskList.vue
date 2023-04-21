<template>
  <div>
    <a-button type="primary" @click="$router.push('/home')">Back to Homepage</a-button>
    <h1>任务列表</h1>
    <a-table :columns="columns" :data-source="tasks" :loading="loading">
      <template v-slot:action="{ record }">
        <span>
          <a-button type="primary" @click="handleView(record.task_id, record.task_type)">
            查看
          </a-button>
          <a-button type="primary" @click="handleAnalyze(record.task_id, record.task_type)">分析</a-button>
          <a-button type="primary" @click="handleResult(record.task_id, record.task_type)">查看分析结果</a-button>
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
    navigateToComponent(taskType) {
      switch (taskType) {
        case "jd_product":
          this.$router.push("/jd_product_list");
          break;
        case "jd_comment":
          this.$router.push("/jd_comment_list");
          break;
        case "weibo_user":
          this.$router.push("/weibo_user_list");
          break;
        case "weibo_comment":
          this.$router.push("/weibo_comment_list");
          break;
        case "weibo_repost":
          this.$router.push("/weibo_repost_list");
          break;
        case "weibo_tweet":
          this.$router.push("/weibo_tweet_list");
          break;
        case "weibo_fan":
          this.$router.push("/weibo_fan_list");
          break;
        case "weibo_follower":
          this.$router.push("/weibo_follower_list");
          break;
        case "weibo_search":
          this.$router.push("/weibo_search_list");
          break;
        default:
          // handle unknown task type
          break;
      }
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

  },
};
</script>
