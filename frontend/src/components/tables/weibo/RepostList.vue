<template>
  <div>
    <a-button type="primary" @click="$router.push('/home')">回到主页</a-button>
    <a-input v-model:value="inputtaskId" placeholder="输入任务ID" @pressEnter="getRepostData" />
    <a-button @click="getRepostData">获取数据</a-button>
    <a-table :columns="columns"
             :dataSource="repostData"
             v-if="repostData.length > 0"/>
  </div>
</template>



<script>
import {Table, Input, Button, message} from 'ant-design-vue';
import axiosInstance from "@/api/axiosInstance";

export default {
  name: 'RepostList',
  components: {
    'a-table': Table,
    'a-input': Input,
    'a-button': Button,
  },
  created() {
    this.getRepostData();
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
      repostData: [],
      columns: [
        {
          title: "ID",
          dataIndex: "_id",
          key: "_id",
        },
        {
          title: "博客ID",
          dataIndex: "mblogid",
          key: "mblogid",
        },
        {
          title: "发布于",
          dataIndex: "created_at",
          key: "created_at",
        },
        {
          title: "Geo",
          dataIndex: "geo",
          key: "geo",
        },
        {
          title: "IP地址",
          dataIndex: "ip_location",
          key: "ip_location",
        },
        {
          title: "转发量",
          dataIndex: "reposts_count",
          key: "reposts_count",
        },
        {
          title: "评论量",
          dataIndex: "comments_count",
          key: "comments_count",
        },
        {
          title: "Attitudes Count",
          dataIndex: "attitudes_count",
          key: "attitudes_count",
        },
        {
          title: "源",
          dataIndex: "source",
          key: "source",
        },
        {
          title: "内容",
          dataIndex: "content",
          key: "content",
        },
        {
          title: "Is Long Text",
          dataIndex: "isLongText",
          key: "isLongText",
        },
        {
          title: "User ID",
          dataIndex: ["user", "_id"],
          key: "user_id",
        },
        {
          title: "Avatar",
          dataIndex: ["fan_info", "avatar_hd"],
          key: "avatar",
        },
        {
          title: "昵称",
          dataIndex: ["user", "nick_name"],
          key: "nick_name",
        },
        {
          title: "Verified",
          dataIndex: ["user", "verified"],
          key: "verified",
        },
        {
          title: "Mbrank",
          dataIndex: ["user", "mbrank"],
          key: "mbrank",
        },
        {
          title: "Mbtype",
          dataIndex: ["user", "mbtype"],
          key: "mbtype",
        },
        {
          title: "URL",
          dataIndex: "url",
          key: "url",
        },
        {
          title: "数据收集时间",
          dataIndex: "crawl_time",
          key: "crawl_time",
        },
      ],
    };
  },
  methods: {
    getRepostData() {
      this.idToFetch = this.inputtaskId || this.taskId;
      axiosInstance.get(`/weibo/data/repost/${this.idToFetch}`).then(response => {
        this.repostData = response.data;
        message.success('加载数据成功!')
        console.log(JSON.stringify(this.repostData))
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
