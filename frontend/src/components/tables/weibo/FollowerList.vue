<template>
  <div>
    <a-button type="primary" @click="$router.push('/home')">回到主页</a-button>
    <a-input v-model:value="inputtaskId" placeholder="输入任务ID" @pressEnter="getFollowerData" />
    <a-button @click="getFollowerData">获取数据</a-button>
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
  created() {
    this.getFollowerData();
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
      followerData: [],
      columns: [
        {
          title: "ID",
          dataIndex: "_id",
          key: "_id",
        },
        {
          title: "粉丝ID",
          dataIndex: "fan_id",
          key: "fan_id",
        },
        {
          title: "关注者ID",
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
          title: "昵称",
          dataIndex: ["follower_info", "nick_name"],
          key: "nick_name",
        },
        {
          title: "Verified",
          dataIndex: ["follower_info", "verified"],
          key: "verified",
        },
        {
          title: "描述",
          dataIndex: ["follower_info", "description"],
          key: "description",
        },
        {
          title: "关注者数量",
          dataIndex: ["follower_info", "followers_count"],
          key: "followers_count",
        },
        {
          title: "Statuses Count",
          dataIndex: ["follower_info", "statuses_count"],
          key: "statuses_count",
        },
        {
          title: "性别",
          dataIndex: ["follower_info", "gender"],
          key: "gender",
        },
        {
          title: "位置",
          dataIndex: ["follower_info", "location"],
          key: "location",
        },
        {
          title: "信用分",
          dataIndex: ["follower_info", "credit_score"],
          key: "credit_score",
        },
        {
          title: "认证种类",
          dataIndex: ["follower_info", "verified_type"],
          key: "verified_type",
        },
        {
          title: "认证原因",
          dataIndex: ["follower_info", "verified_reason"],
          key: "verified_reason",
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
    getFollowerData() {
      this.idToFetch = this.inputtaskId || this.taskId;
      axiosInstance.get(`/weibo/data/follower/${this.idToFetch}`).then(response => {
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
