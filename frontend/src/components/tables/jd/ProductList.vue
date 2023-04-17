<template>
  <div>
    <a-button type="primary" @click="$router.push('/home')">回到主页</a-button>
    <a-input v-model:value="inputtaskId" placeholder="Enter Task ID" @pressEnter="getProductData" />
    <a-button @click="getProductData">获取数据</a-button>
    <a-table :columns="columns"
             :dataSource="productData"
             v-if="productData.length > 0"/>
  </div>
</template>

<script>
import {Table, Input, Button, message} from 'ant-design-vue';
import axiosInstance from "@/api/axiosInstance";

export default {
  name: 'ProductList',
  components: {
    'a-table': Table,
    'a-input': Input,
    'a-button': Button,
  },
  created() {
    this.getProductData();
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
      productData: [],
      columns: [],
    };
  },
  methods: {
    getProductData() {
      this.idToFetch = this.inputtaskId || this.taskId;
      axiosInstance.get(`/jd/data/product/${this.idToFetch}`).then(response => {
        const rawData = response.data;
        this.productData = rawData.map(item => {
          const contentObj = item.name.reduce((acc, name, index) => {
            acc[name] = item.content[index];
            return acc;
          }, {});
          return {
            ...contentObj,
            _id: item._id,
            url: item.url,
          };
        });
        const columns = rawData[0].name.map((header) => ({
          title: header,
          dataIndex: header,
          key: header,
        }));
        columns.unshift({
          title: 'ID',
          dataIndex: '_id',
          key: '_id'
        });
        columns.push({
          title: 'URL',
          dataIndex: 'url',
          key: 'url'
        });
        this.columns = columns;
        message.success('加载数据成功!');
      }).catch(error => {
        message.error('加载数据失败!');
        console.log(error);
      });
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
