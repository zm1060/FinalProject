<template>
  <div>
    <a-input v-model:value="taskId" placeholder="Enter Task ID" @pressEnter="getCommentData" />
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
  name: 'CommentList',
  components: {
    'a-table': Table,
    'a-input': Input,
    'a-button': Button,
  },
  data() {
    return {
      taskId: '',
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
          title: "Like Counts",
          dataIndex: "like_counts",
          key: "like_counts",
        },
        {
          title: "IP Location",
          dataIndex: "ip_location",
          key: "ip_location",
        },
        {
          title: "Content",
          dataIndex: "content",
          key: "content",
        },
        {
          title: "Comment User ID",
          dataIndex: ["comment_user", "_id"],
          key: "comment_user_id",
        },
        {
          title: "Comment User Avatar",
          dataIndex: ["comment_user", "avatar_hd"],
          key: "comment_user_avatar",
        },
        {
          title: "Comment User Nick Name",
          dataIndex: ["comment_user", "nick_name"],
          key: "comment_user_nick_name",
        },
        {
          title: "Comment User Verified",
          dataIndex: ["comment_user", "verified"],
          key: "comment_user_verified",
        },
        {
          title: "Comment User Description",
          dataIndex: ["comment_user", "description"],
          key: "comment_user_description",
        },
        {
          title: "Comment User Followers Count",
          dataIndex: ["comment_user", "followers_count"],
          key: "comment_user_followers_count",
        },
        {
          title: "Comment User Friends Count",
          dataIndex: ["comment_user", "friends_count"],
          key: "comment_user_friends_count",
        },
        {
          title: "Comment User Statuses Count",
          dataIndex: ["comment_user", "statuses_count"],
          key: "comment_user_statuses_count",
        },
        {
          title: "Comment User Gender",
          dataIndex: ["comment_user", "gender"],
          key: "comment_user_gender",
        },
        {
          title: "Comment User Location",
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
      axiosInstance.get(`/weibo/data/comment/${this.taskId}`).then(response => {
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
