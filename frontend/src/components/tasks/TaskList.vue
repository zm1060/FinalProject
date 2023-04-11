<template>
  <div>
    <h1>My Tasks</h1>
    <a-table :columns="columns" :data-source="tasks"></a-table>
  </div>
</template>

<script>
import {message, Table} from "ant-design-vue";
import axiosInstance from "@/api/axiosInstance";

export default {
  name: "MyTasks",
  components: {
    "a-table": Table,
  },
  data() {
    return {
      tasks: [],
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
      ],
    };
  },
  created() {
    this.fetchTasks();
  },
  methods: {
    fetchTasks() {
      axiosInstance.get("/user/tasks").then((response) => {
        this.tasks = response.data;
        message.success("加载任务列表成功!")
      }).catch(error => {
        message.error('加载失败!(当前用户token过期)')
        console.log(error)
      });
    },
  },
};
</script>
