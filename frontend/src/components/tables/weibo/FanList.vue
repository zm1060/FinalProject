<template>
  <div>
    <a-button type="primary" @click="$router.push('/home')">Back to Homepage</a-button>
    <a-input v-model:value="inputtaskId" placeholder="Enter Task ID" @pressEnter="getFanData" />
    <a-button @click="getFanData">Fetch Data</a-button>
    <a-table :columns="columns"
             :dataSource="fanData"
             v-if="fanData.length > 0"/>
  </div>
</template>



<script>
import {Table, Input, Button, message, Tooltip} from 'ant-design-vue';
import axiosInstance from "@/api/axiosInstance";

export default {
  name: 'FanList',
  components: {
    'a-table': Table,
    'a-input': Input,
    'a-button': Button,
  },
  created() {
    this.getFanData();
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
      fanData: [],
      columns: [
        {
          title: "ID",
          dataIndex: "_id",
          key: "_id",
        },
        {
          title: "Follower ID",
          dataIndex: "follower_id",
          key: "follower_id",
        },
        {
          title: "Fan ID",
          dataIndex: ["fan_info", "_id"],
          key: "fan_id",
        },
        {
          title: "Avatar",
          dataIndex: ["fan_info", "avatar_hd"],
          key: "avatar",
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
          dataIndex: ["fan_info", "nick_name"],
          key: "nick_name",
        },
        {
          title: "Verified",
          dataIndex: ["fan_info", "verified"],
          key: "verified",
        },
        {
          title: "Description",
          dataIndex: ["fan_info", "description"],
          key: "description",
        },
        {
          title: "Followers Count",
          dataIndex: ["fan_info", "followers_count"],
          key: "followers_count",
        },
        {
          title: "Friends Count",
          dataIndex: ["fan_info", "friends_count"],
          key: "friends_count",
        },
        {
          title: "Statuses Count",
          dataIndex: ["fan_info", "statuses_count"],
          key: "statuses_count",
        },
        {
          title: "Gender",
          dataIndex: ["fan_info", "gender"],
          key: "gender",
        },
        {
          title: "Location",
          dataIndex: ["fan_info", "location"],
          key: "location",
        },
        {
          title: "MB Rank",
          dataIndex: ["fan_info", "mbrank"],
          key: "mbrank",
        },
        {
          title: "MB Type",
          dataIndex: ["fan_info", "mbtype"],
          key: "mbtype",
        },
        {
          title: "Credit Score",
          dataIndex: ["fan_info", "credit_score"],
          key: "credit_score",
        },
        {
          title: "Created At",
          dataIndex: ["fan_info", "created_at"],
          key: "created_at",
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
    getFanData() {
      this.idToFetch = this.inputtaskId || this.taskId;
      axiosInstance.get(`/weibo/data/fan/${this.idToFetch}`).then(response => {
        this.fanData = response.data;
        message.success('加载数据成功!')
        console.log(JSON.stringify(this.fanData))
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
