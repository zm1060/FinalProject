<template>
  <div>
    <a-button type="primary" @click="$router.push('/home')">Back to Homepage</a-button>
    <a-input v-model:value="inputtaskId" placeholder="Enter Task ID" @pressEnter="getCommentData" />
    <a-button @click="getCommentData">Fetch Data</a-button>
    <a-table :columns="columns"
             :dataSource="commentData"
             v-if="commentData.length > 0"/>
  </div>
</template>



<script>
import {Table, Input, Button, message} from 'ant-design-vue';
import axiosInstance from "@/api/axiosInstance";

export default {
  name: 'JDCommentList',
  components: {
    'a-table': Table,
    'a-input': Input,
    'a-button': Button,
  },
  created() {
    this.getCommentData();
  },
  computed: {
    taskId() {
      return this.$route.params.taskId;
    },
  },
  data() {
    return {
      inputtaskId: '',
      idToFetch: '',
      commentData: [],
      columns: [
        {
          title: "ID",
          dataIndex: "_id",
          key: "_id",
        },
        {
          title: "产品名称",
          dataIndex: "name",
          key: "name",
        },
        {
          title: "产品链接",
          dataIndex: "url",
          key: "url",
        },
        {
          title: "Date",
          dataIndex: "date",
          key: "date",
        },
        {
          title: "Content",
          dataIndex: "content",
          key: "content",
        },
      ],
    };
  },
  methods: {
    getCommentData() {
      this.idToFetch = this.inputtaskId || this.taskId;
      axiosInstance.get(`/jd/data/comment/${this.idToFetch}`).then(response => {
        this.commentData = response.data;
        message.success('加载数据成功!')
        console.log(JSON.stringify(this.commentData))
      }).catch(error => {
        message.error('加载数据失败!')
        console.log(error)
      })

    },
  },
};
</script>

<style>
.user-list {
  margin: 20px;
}

ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

li {
  margin-bottom: 20px;
}

h3 {
  margin: 0;
}
</style>
