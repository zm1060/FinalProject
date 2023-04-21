<template>
  <div>
    <a-button type="primary" @click="$router.push('/home')">回到主页</a-button>
    <a-input v-model:value="inputtaskId" placeholder="输入任务ID" @pressEnter="getFanData" />
    <a-button @click="getFanData">获取数据</a-button>
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
          title: "关注者ID",
          dataIndex: "follower_id",
          key: "follower_id",
        },
        {
          title: "粉丝ID",
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
          title: "昵称",
          dataIndex: ["fan_info", "nick_name"],
          key: "nick_name",
        },
        {
          title: "Verified",
          dataIndex: ["fan_info", "verified"],
          key: "verified",
        },
        {
          title: "描述",
          dataIndex: ["fan_info", "description"],
          key: "description",
        },
        {
          title: "粉丝数量",
          dataIndex: ["fan_info", "followers_count"],
          key: "followers_count",
        },
        {
          title: "朋友数量",
          dataIndex: ["fan_info", "friends_count"],
          key: "friends_count",
        },
        {
          title: "Statuses Count",
          dataIndex: ["fan_info", "statuses_count"],
          key: "statuses_count",
        },
        {
          title: "性别",
          dataIndex: ["fan_info", "gender"],
          key: "gender",
        },
        {
          title: "位置",
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
          title: "信用分",
          dataIndex: ["fan_info", "credit_score"],
          key: "credit_score",
        },
        {
          title: "账号创立时间",
          dataIndex: ["fan_info", "created_at"],
          key: "created_at",
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
