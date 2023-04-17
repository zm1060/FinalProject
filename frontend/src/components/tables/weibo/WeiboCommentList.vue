<template>
  <div>
    <a-button type="primary" @click="$router.push('/home')">回到主页</a-button>
    <a-input v-model:value="inputtaskId" placeholder="Enter Task ID" @pressEnter="getCommentData" />
    <a-button @click="getCommentData">获取数据</a-button>
    <a-table :columns="columns"
             :dataSource="commentData"
             v-if="commentData.length > 0"/>
  </div>
</template>



<script>
import {Table, Input, Button, message} from 'ant-design-vue';
import axiosInstance from "@/api/axiosInstance";

export default {
  name: 'WeiboCommentList',
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
          title: "Created At",
          dataIndex: "created_at",
          key: "created_at",
        },
        {
          title: "点赞数量",
          dataIndex: "like_counts",
          key: "like_counts",
        },
        {
          title: "IP地址",
          dataIndex: "ip_location",
          key: "ip_location",
        },
        {
          title: "内容",
          dataIndex: "content",
          key: "content",
        },
        {
          title: "评论者ID",
          dataIndex: ["comment_user", "_id"],
          key: "comment_user_id",
        },
        {
          title: "评论者Avatar",
          dataIndex: ["comment_user", "avatar_hd"],
          key: "comment_user_avatar",
        },
        {
          title: "评论者昵称",
          dataIndex: ["comment_user", "nick_name"],
          key: "comment_user_nick_name",
        },
        {
          title: "评论者Verified",
          dataIndex: ["comment_user", "verified"],
          key: "comment_user_verified",
        },
        {
          title: "评论者描述",
          dataIndex: ["comment_user", "description"],
          key: "comment_user_description",
        },
        {
          title: "评论者关注者数量",
          dataIndex: ["comment_user", "followers_count"],
          key: "comment_user_followers_count",
        },
        {
          title: "评论者朋友数量",
          dataIndex: ["comment_user", "friends_count"],
          key: "comment_user_friends_count",
        },
        {
          title: "Comment User Statuses Count",
          dataIndex: ["comment_user", "statuses_count"],
          key: "comment_user_statuses_count",
        },
        {
          title: "评论者性别",
          dataIndex: ["comment_user", "gender"],
          key: "comment_user_gender",
        },
        {
          title: "评论者位置",
          dataIndex: ["comment_user", "location"],
          key: "comment_user_location",
        },
        {
          title: "Comment User MBRank",
          dataIndex: ["comment_user", "mbrank"],
          key: "comment_user_mbrank",
        },
        {
          title: "Comment User MBType",
          dataIndex: ["comment_user", "mbtype"],
          key: "comment_user_mbtype",
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
    getCommentData() {
      this.idToFetch = this.inputtaskId || this.taskId;
      axiosInstance.get(`/weibo/data/comment/${this.idToFetch}`).then(response => {
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
