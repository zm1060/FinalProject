<template>
  <div>
    <a-button type="primary" @click="$router.push('/home')">回到主页</a-button>
    <a-input v-model:value="inputtaskId" placeholder="Enter Task ID" @pressEnter="getUserData" />
    <a-button @click="getUserData">获取数据</a-button>
    <a-table :columns="columns"
             :dataSource="userData"
             v-if="userData.length > 0"/>
  </div>
</template>

<script>
import {Table, Input, Button, message} from 'ant-design-vue';
import axiosInstance from "@/api/axiosInstance";

export default {
  name: 'UserList',
  components: {
    'a-table': Table,
    'a-input': Input,
    'a-button': Button,
  },
  created() {
    this.getUserData();
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
      userData: [],
      columns: [
        {
          title: 'Avatar',
          dataIndex: 'avatar_hd',
          scopedSlots: { customRender: 'avatar' },
        },
        {
          title: '昵称',
          dataIndex: 'nick_name',
        },
        {
          title: '地址',
          dataIndex: 'location',
        },
        {
          title: '性别',
          dataIndex: 'gender',
        },
        {
          title: '关注数量',
          dataIndex: 'followers_count',
        },
        {
          title: '朋友数量',
          dataIndex: 'friends_count',
        },
        {
          title: 'Statuses Count',
          dataIndex: 'statuses_count',
        },
        {
          title: '验证原因',
          dataIndex: 'verified_reason',
        },
        {
          title: '生日',
          dataIndex: 'birthday',
        },
        {
          title: 'Created At',
          dataIndex: 'created_at',
        },
        {
          title: 'Description Text',
          dataIndex: 'desc_text',
        },
        {
          title: 'IP地址',
          dataIndex: 'ip_location',
        },
        {
          title: 'Sunshine Credit',
          dataIndex: 'sunshine_credit',
        },
        {
          title: 'Label Desc',
          dataIndex: 'label_desc',
          scopedSlots: { customRender: 'label_desc' },
        },
        {
          title: 'Crawl Time',
          dataIndex: 'crawl_time',
          slots: { customRender: 'crawl_time' },
        },
      ],

    };
  },
  methods: {
    getUserData() {
      this.idToFetch = this.inputtaskId || this.taskId;
      axiosInstance.get(`/weibo/data/user/${this.idToFetch}`).then(response => {
        this.userData = [response.data];
        message.success('加载数据成功!')
        console.log(response)
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
