<template>
  <div>
    <a-button type="primary" @click="$router.push('/home')">回到主页</a-button>
    <a-input v-model:value="inputtaskId" placeholder="输入任务ID" @pressEnter="getCommentData" />
    <a-button @click="getCommentData">获取数据</a-button>
    <a-input v-model:value="searchQuery" placeholder="输入搜索关键字" />
    <a-button @click="updateFilteredData()">搜索</a-button>
    <a-button @click="searchQuery = ''">重置</a-button>
    <a-table :columns="columns"
             :dataSource="commentData"
             v-if="commentData.length > 0"/>
  </div>
</template>

<script>
import {Table, Input, Button, message} from 'ant-design-vue';
import axiosInstance from "@/api/axiosInstance";

export default {
  name: 'JDCommentList',
  components: {
    'a-table': Table,
    'a-input': Input,
    'a-button': Button,
  },
  created() {
    this.getCommentData();
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
      commentData: [],
      searchQuery: "",
      columns: [
        {
          title: "ID",
          dataIndex: "_id",
          key: "_id",
        },
        {
          title: "产品名称",
          dataIndex: "name",
          key: "name",
        },
        {
          title: "产品链接",
          dataIndex: "url",
          key: "url",
        },
        {
          title: "日期",
          dataIndex: "date",
          key: "date",
        },
        {
          title: "评论内容",
          dataIndex: "content",
          key: "content",
        },
      ],
    };
  },
  methods: {
    async getCommentData() {
      this.idToFetch = this.inputtaskId || this.taskId;
      axiosInstance.get(`/jd/data/comment/${this.idToFetch}`).then(response => {
        this.commentData = response.data;
        message.success('加载数据成功!')
        console.log(JSON.stringify(this.commentData))
      }).catch(error => {
        message.error('加载数据失败!')
        console.log(error)
      })

    },
    searchCommentData() {
      const searchQuery = this.searchQuery.trim();
      if (searchQuery === "") {
        return this.commentData;
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

        const filteredData = this.commentData.filter(record => {
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
        this.getCommentData();
      } else {
        this.commentData = this.searchCommentData();
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
