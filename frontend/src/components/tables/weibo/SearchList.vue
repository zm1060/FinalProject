<template>
  <div>
    <a-button type="primary" @click="$router.push('/home')">回到主页</a-button>
    <a-input v-model:value="inputtaskId" placeholder="输入任务ID" @pressEnter="getSearchData" />
    <a-button @click="getSearchData">获取数据</a-button>
    <a-table :columns="columns"
             :dataSource="searchData"
              v-if="searchData.length > 0"/>
  </div>
</template>

<script>
import {Table, Input, Button, message} from 'ant-design-vue';
import axiosInstance from "@/api/axiosInstance";
import {toRaw} from "vue";

export default {
  name: 'SearchList',
  components: {
    'a-table': Table,
    'a-input': Input,
    'a-button': Button,
  },
  created() {
    this.getSearchData();
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
      searchData: [],
      columns: [
        {
          title: "ID",
          dataIndex: "_id",
          key: "_id",
        },
        {
          title: "Avatar",
          dataIndex: "avatar_hd",
          key: "follower_avatar",
        },
        {
          title: "关键字",
          dataIndex: "keyword",
          key: "keyword"
        },
        {
          title: "博客ID",
          dataIndex: "mblogid",
          key: "mblogid"
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
          title: "用户",
          dataIndex: "user",
          key: "user"
        },
        {
          title: "描述",
          dataIndex: "description",
          key: "description",
        },
        {
          title: "关注数量",
          dataIndex: "followers_count",
          key: "followers_count",
        },
        {
          title: "朋友数量",
          dataIndex: "friends_count",
          key: "friends_count",
        },
        {
          title: "Statuses Count",
          dataIndex: "status_count",
          key: "status_count",
        },
        {
          title: "性别",
          dataIndex: "gender",
          key: "gender",
        },
        {
          title: "位置",
          dataIndex: "location",
          key: "location",
        },
        {
          title: "认证种类",
          dataIndex: "verified_type",
          key: "verified_type",
        },
        {
          title: "认证原因",
          dataIndex: "verified_reason",
          key: "verified_reason",
        },
        {
          title: "生日",
          dataIndex: "birthday",
          key: "birthday",
        },
        {
          title: "账号创立时间",
          dataIndex: "created_at",
          key: "created_at",
        },
        {
          title: "描述文本",
          dataIndex: "desc_text",
          key: "desc_text",
        },
        {
          title: "IP地址",
          dataIndex: "ip_location",
          key: "ip_location",
        },
        {
          title: "阳光信用分",
          dataIndex: "sunshine_credit",
          key: "sunshine_credit",
        },
        {
          title: "标签描述",
          dataIndex: "label_desc",
          key: "label_desc",
        },
        {
          title: "公司",
          dataIndex: "company",
          key: "company",
        },
        {
          title: "教育",
          dataIndex: ["eduction", "school"],
          key: "eduction",
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
    getSearchData() {
      this.idToFetch = this.inputtaskId || this.taskId;
      axiosInstance.get(`/weibo/data/search/${this.idToFetch}`).then(response => {
        this.searchData = response.data;
        console.log(toRaw(this.searchData)); // access the raw array data
        message.success('加载数据成功!')
      }).catch(error => {
        message.error('加载数据失败!')
        console.log(error)
      })

    },
  },
};
</script>

<style>
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
