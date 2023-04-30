<template>
  <div>
    <a-button type="primary" @click="$router.push('/home')">回到主页</a-button>
    <a-input v-model:value="inputtaskId" placeholder="输入任务ID" @pressEnter="getSearchData" />
    <a-button @click="getSearchData">获取数据</a-button>

    <a-input v-model:value="searchQuery" placeholder="输入搜索关键字" />
    <a-button @click="updateFilteredData()">搜索</a-button>
    <a-button @click="searchQuery = ''">重置</a-button>
    <a-table :columns="columns"
             :dataSource="searchData"
              v-if="searchData.length > 0"/>
  </div>
</template>

<script>
import {Table, Input, Button, message} from 'ant-design-vue';
import axiosInstance from "@/api/axiosInstance";

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
  watch: {
    searchQuery() {
      this.updateFilteredData();
    }
  },
  data() {
    return {
      inputtaskId: '',
      idToFetch: '',
      searchData: [],
      searchQuery: "",
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
          title: "转发数量",
          dataIndex: "reposts_count",
          key: "reposts_count",
        },
        {
          title: "评论数量",
          dataIndex: "comments_count",
          key: "comments_count",
        },
        {
          title: "参与数量",
          dataIndex: "attitudes_count",
          key: "attitudes_count",
        },
        {
          title: "发布时间",
          dataIndex: "created_at",
          key: "created_at",
        },
        {
          title: "用户ID",
          dataIndex: ["user","_id"],
          key: "user"
        },
        {
          title: "用户昵称",
          dataIndex: ["user","nick_name"],
          key: "description",
        },
        {
          title: "用户认证种类",
          dataIndex: ["user","verified_type"],
          key: "verified_type",
        },
        {
          title: "IP地址",
          dataIndex: "ip_location",
          key: "ip_location",
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
        message.success('加载数据成功!')
      }).catch(error => {
        message.error('加载数据失败!')
        console.log(error)
      })

    },
    searchSearchData() {
      const searchQuery = this.searchQuery.trim();
      if (searchQuery === "") {
        return this.searchData;
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

        const filteredData = this.searchData.filter(record => {
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
        this.getSearchData();
      } else {
        this.searchData = this.searchSearchData();
      }
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
