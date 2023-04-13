<template>
  <div>
    <a-input v-model:value="taskId" placeholder="Enter Task ID" @pressEnter="getTweetData" />
    <a-button @click="getTweetData">Fetch Data</a-button>
    <a-table :columns="columns"
             :dataSource="tweetData"
             v-if="tweetData.length > 0"/>
  </div>
</template>



<script>
import {Table, Input, Button, message} from 'ant-design-vue';
import axiosInstance from "@/api/axiosInstance";

export default {
  name: 'TweetList',
  components: {
    'a-table': Table,
    'a-input': Input,
    'a-button': Button,
  },
  data() {
    return {
      taskId: '',
      tweetData: [],
      columns: [
        {
          title: "ID",
          dataIndex: "_id",
          key: "_id",
        },
        {
          title: "Blog ID",
          dataIndex: "mblogid",
          key: "mblogid",
        },
        {
          title: "Created At",
          dataIndex: "created_at",
          key: "created_at",
        },
        {
          title: "IP Location",
          dataIndex: "ip_location",
          key: "ip_location",
        },
        {
          title: "Reposts Count",
          dataIndex: "reposts_count",
          key: "reposts_count",
        },
        {
          title: "Comments Count",
          dataIndex: "comments_count",
          key: "comments_count",
        },
        {
          title: "Attitudes Count",
          dataIndex: "attitudes_count",
          key: "attitudes_count",
        },
        {
          title: "Source",
          dataIndex: "source",
          key: "source",
        },
        {
          title: "Content",
          dataIndex: "content",
          key: "content",
        },
        {
          title: "Is Long Text",
          dataIndex: "isLongText",
          key: "isLongText",
        },
        {
          title: "URL",
          dataIndex: "url",
          key: "url",
        },
        {
          title: "Crawl Time",
          dataIndex: "crawl_time",
          key: "crawl_time",
        },
      ],
    };
  },
  methods: {
    getTweetData() {
      axiosInstance.get(`/weibo/data/tweet/${this.taskId}`).then(response => {
        this.tweetData = response.data;
        message.success('加载数据成功!')
        console.log(JSON.stringify(this.tweetData))
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
