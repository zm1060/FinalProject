<template>
  <div>
    <a-input v-model:value="taskId" placeholder="Enter Task ID" @pressEnter="getFollowerData" />
    <a-button @click="getFollowerData">Fetch Data</a-button>
    <a-table :columns="columns"
             :dataSource="followerData"
             v-if="followerData.length > 0"/>
  </div>
</template>



<script>
import {Table, Input, Button, message, Tooltip} from 'ant-design-vue';
import axiosInstance from "@/api/axiosInstance";

export default {
  name: 'FollowerList',
  components: {
    'a-table': Table,
    'a-input': Input,
    'a-button': Button,
  },
  data() {
    return {
      taskId: '',
      followerData: [],
      columns: [
        {
          title: "ID",
          dataIndex: "_id",
          key: "_id",
        },
        {
          title: "Fan ID",
          dataIndex: "fan_id",
          key: "fan_id",
        },
        {
          title: "Follower ID",
          dataIndex: ["follower_info", "_id"],
          key: "follower_id",
        },
        {
          title: "Avatar",
          dataIndex: ["follower_info", "avatar_hd"],
          key: "follower_avatar",
          customRender: (text) => {
            if (text.length > 20) {
              return (
                <Tooltip title={text}>
                  {text.slice(0, 20)}...
                </Tooltip>
              );
            } else {
              return text;
            }
          }
        },
        {
          title: "Nick Name",
          dataIndex: ["follower_info", "nick_name"],
          key: "nick_name",
        },
        {
          title: "Verified",
          dataIndex: ["follower_info", "verified"],
          key: "verified",
        },
        {
          title: "Description",
          dataIndex: ["follower_info", "description"],
          key: "description",
        },
        {
          title: "Followers Count",
          dataIndex: ["follower_info", "followers_count"],
          key: "followers_count",
        },
        {
          title: "Statuses Count",
          dataIndex: ["follower_info", "statuses_count"],
          key: "statuses_count",
        },
        {
          title: "Gender",
          dataIndex: ["follower_info", "gender"],
          key: "gender",
        },
        {
          title: "Location",
          dataIndex: ["follower_info", "location"],
          key: "location",
        },
        {
          title: "Credit Score",
          dataIndex: ["follower_info", "credit_score"],
          key: "credit_score",
        },
        {
          title: "Verified Type",
          dataIndex: ["follower_info", "verified_type"],
          key: "verified_type",
        },
        {
          title: "Verified Type",
          dataIndex: ["follower_info", "verified_reason"],
          key: "verified_reason",
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
    getFollowerData() {
      axiosInstance.get(`/weibo/data/follower/${this.taskId}`).then(response => {
        this.followerData = response.data;
        message.success('加载数据成功!')
        console.log(JSON.stringify(this.followerData))
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
