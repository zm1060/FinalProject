<template>
  <div>
    <a-button type="primary" @click="$router.push('/home')">回到主页</a-button>
    <a-input v-model:value="inputtaskId" placeholder="输入任务ID" @pressEnter="getTweetData" />
    <a-button @click="getTweetData">获取数据</a-button>

    <a-input v-model:value="searchQuery" placeholder="输入搜索关键字" />
    <a-button @click="updateFilteredData()">搜索</a-button>
    <a-button @click="searchQuery = ''">重置</a-button>
    <a-table :columns="columns"
             :dataSource="tweetData"
             v-if="tweetData.length > 0"/>
  </div>
</template>

<script>
import {Table, Input, Button, message} from 'ant-design-vue';
import axiosInstance from "@/api/axiosInstance";

export default {
  name: 'TweetList',
  components: {
    'a-table': Table,
    'a-input': Input,
    'a-button': Button,
  },
  created() {
    this.getTweetData();
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
      tweetData: [],
      searchQuery: "",
      columns: [
        {
          title: "ID",
          dataIndex: "_id",
          key: "_id",
        },
        {
          title: "博客ID",
          dataIndex: "mblogid",
          key: "mblogid",
        },
        {
          title: "发布于",
          dataIndex: "created_at",
          key: "created_at",
        },
        {
          title: "IP地址",
          dataIndex: "ip_location",
          key: "ip_location",
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
          title: "参与者数量",
          dataIndex: "attitudes_count",
          key: "attitudes_count",
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
          title: "Is Long Text",
          dataIndex: "isLongText",
          key: "isLongText",
        },
        {
          title: "URL",
          dataIndex: "url",
          key: "url",
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
    getTweetData() {
      this.idToFetch = this.inputtaskId || this.taskId;
      axiosInstance.get(`/weibo/data/tweet/${this.idToFetch}`).then(response => {
        this.tweetData = response.data;
        message.success('加载数据成功!')
      }).catch(error => {
        message.error('加载数据失败!')
        console.log(error)
      })
    },
    searchTweetData() {
      const searchQuery = this.searchQuery.trim();
      if (searchQuery === "") {
        return this.tweetData;
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

        const filteredData = this.tweetData.filter(record => {
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
        this.getTweetData();
      } else {
        this.tweetData = this.searchTweetData();
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
