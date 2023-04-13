<template>
  <div>
    <a-input v-model:value="taskId" placeholder="Enter Task ID" @pressEnter="getProductData" />
    <a-button @click="getProductData">Fetch Data</a-button>
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
  data() {
    return {
      taskId: '',
      productData: [],
      columns: [],
    };
  },
  methods: {
    getProductData() {
      axiosInstance.get(`/jd/data/product/${this.taskId}`).then(response => {
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
