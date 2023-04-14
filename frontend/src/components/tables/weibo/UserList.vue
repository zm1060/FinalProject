<template>
  <div>
    <a-button type="primary" @click="$router.push('/home')">Back to Homepage</a-button>
    <a-input v-model:value="inputtaskId" placeholder="Enter Task ID" @pressEnter="getUserData" />
    <a-button @click="getUserData">Fetch Data</a-button>
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
          title: 'Name',
          dataIndex: 'nick_name',
        },
        {
          title: 'Location',
          dataIndex: 'location',
        },
        {
          title: 'Gender',
          dataIndex: 'gender',
        },
        {
          title: 'Followers Count',
          dataIndex: 'followers_count',
        },
        {
          title: 'Friends Count',
          dataIndex: 'friends_count',
        },
        {
          title: 'Statuses Count',
          dataIndex: 'statuses_count',
        },
        {
          title: 'Verified Reason',
          dataIndex: 'verified_reason',
        },
        {
          title: 'Birthday',
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
          title: 'IP Location',
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
