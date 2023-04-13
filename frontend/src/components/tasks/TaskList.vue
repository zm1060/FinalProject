<template>
  <div>
    <router-link to="/home">返回主页</router-link>
    <h1>My Tasks</h1>
    <a-table :columns="columns" :data-source="tasks" :loading="loading">
      <template v-slot:action="{ record }">
        <span>
          <a-button type="primary" @click="handleView(record.task_id)">
            View
          </a-button>
          <a-popconfirm
            title="Are you sure to delete this task?"
            @confirm="handleDelete(record.task_id)"
          >
            <a-button type="danger">Delete</a-button>
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
          title: "Task ID",
          dataIndex: "task_id",
          key: "task_id",
        },
        {
          title: "Task Type",
          dataIndex: "task_type",
          key: "task_type",
        },
        {
          title: "Task Time",
          dataIndex: "task_time",
          key: "task_time",
        },
        {
          title: "Finish Time",
          dataIndex: ["stats", "finish_time"],
          key: "finish_time",
        },
        {
          title: "Item Scraped Count",
          dataIndex: ["stats", "item_scraped_count"],
          key: "item_scraped_count",
        },
        {
          title: "Action",
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
    handleView(taskId) {
      // Navigate to the view task page with the given taskId
      this.$router.push(`/view-task/${taskId}`);
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
  },
};
</script>
