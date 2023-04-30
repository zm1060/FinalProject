<template>
  <div>
    <a-button type="primary" @click="$router.push('/home')">回到主页</a-button>
    <a-input v-model:value="inputtaskId" placeholder="输入任务ID" @pressEnter="getUserData" />
    <a-button @click="getUserData">获取数据</a-button>

    <a-input v-model:value="searchQuery" placeholder="输入搜索关键字" />
    <a-button @click="updateFilteredData()">搜索</a-button>
    <a-button @click="searchQuery = ''">重置</a-button>
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
  watch: {
    searchQuery() {
      this.updateFilteredData();
    }
  },
  data() {
    return {
      inputtaskId: '',
      idToFetch: '',
      userData: [],
      searchQuery: "",
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
          title: '账号创立时间',
          dataIndex: 'created_at',
        },
        {
          title: '描述文本',
          dataIndex: 'desc_text',
        },
        {
          title: 'IP地址',
          dataIndex: 'ip_location',
        },
        {
          title: '阳光信用分',
          dataIndex: 'sunshine_credit',
        },
        {
          title: '标签描述',
          dataIndex: 'label_desc',
          scopedSlots: { customRender: 'label_desc' },
        },
        {
          title: '数据收集时间',
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
        this.userData = [response.data][0];
        message.success('加载数据成功!')
        console.log(response)
      }).catch(error => {
        message.error('加载数据失败!')
        console.log(error)
      })
    },
    searchUserData() {
      const searchQuery = this.searchQuery.trim();
      if (searchQuery === "") {
        return this.userData;
      } else {
        const getValue = (record, dataIndex) => {
          if (Array.isArray(dataIndex)) {
            let value = record;
            dataIndex.forEach(key => {
              value = value[key];
            });
            return value;
          }
          return record[dataIndex];
        };
        const filteredData = this.userData.filter(record => {
          return this.columns.some(column => {
            const dataIndex = column.dataIndex;
            const value = getValue(record, dataIndex);
            const searchRegex = new RegExp(searchQuery, "giu");
            return searchRegex.test(value);
          });
        });
        return filteredData;
      }
    },
    updateFilteredData() {
      if (this.searchQuery === "") {
        this.getUserData();
      } else {
        this.userData = this.searchUserData();
      }
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