<template>
  <div>
    <a-input v-model:value="taskId" placeholder="Enter Task ID" @pressEnter="getSearchData" />
    <a-button @click="getSearchData">Fetch Data</a-button>
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
  data() {
    return {
      taskId: '',
      searchData: [],
      columns: [
        {
          title: "ID",
          dataIndex: "_id",
          scopedSlots: { customRender: "content" }
        },
        {
          title: "MBlog ID",
          dataIndex: "mblogid",
          scopedSlots: { customRender: "content" }
        },
        {
          title: "Created At",
          dataIndex: "created_at",
          scopedSlots: { customRender: "content" }
        },
        {
          title: "Geo",
          dataIndex: "geo",
          scopedSlots: { customRender: "content" }
        },
        {
          title: "IP Location",
          dataIndex: "ip_location",
          scopedSlots: { customRender: "content" }
        },
        {
          title: "Reposts Count",
          dataIndex: "reposts_count",
          scopedSlots: { customRender: "content" }
        },
        {
          title: "Comments Count",
          dataIndex: "comments_count",
          scopedSlots: { customRender: "content" }
        },
        {
          title: "Attitudes Count",
          dataIndex: "attitudes_count",
          scopedSlots: { customRender: "content" }
        },
        {
          title: "Source",
          dataIndex: "source",
          scopedSlots: { customRender: "content" }
        },
        {
          title: "Content",
          dataIndex: "content",
          scopedSlots: { customRender: "content" }
        },
        {
          title: "Pic URLs",
          dataIndex: "pic_urls",
          scopedSlots: { customRender: "content" }
        },
        {
          title: "Pic Number",
          dataIndex: "pic_num",
          scopedSlots: { customRender: "content" }
        },
        {
          title: "Is Long Text",
          dataIndex: "isLongText",
          scopedSlots: { customRender: "content" }
        },
        {
          title: "User",
          dataIndex: "user",
          scopedSlots: { customRender: "content" }
        },
        {
          title: "URL",
          dataIndex: "url",
          scopedSlots: { customRender: "content" }
        },
        {
          title: "Keyword",
          dataIndex: "keyword",
          scopedSlots: { customRender: "content" }
        },
        {
          title: "Crawl Time",
          dataIndex: "crawl_time",
          scopedSlots: { customRender: "content" }
        }
      ],

    };
  },
  methods: {
    getSearchData() {
      axiosInstance.get(`/weibo/data/search/${this.taskId}`).then(response => {
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
