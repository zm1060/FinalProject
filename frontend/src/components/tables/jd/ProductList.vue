<template>
  <div>
    <a-button type="primary" @click="$router.push('/home')">回到主页</a-button>
    <a-input v-model:value="inputtaskId" placeholder="输入任务ID" @pressEnter="getProductData" />
    <a-button @click="getProductData">获取数据</a-button>
    <a-input v-model:value="searchQuery" placeholder="输入搜索关键字" />
    <a-button @click="updateFilteredData()">搜索</a-button>
    <a-button @click="searchQuery = ''">重置</a-button>
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
  watch: {
    searchQuery() {
      this.updateFilteredData();
    }
  },
  data() {
    return {
      inputtaskId: '',
      idToFetch: '',
      productData: [],
      searchQuery: "",
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
    searchProductData() {
      const searchQuery = this.searchQuery.trim();
      if (searchQuery === "") {
        return this.productData;
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

        const filteredData = this.productData.filter(record => {
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
        this.getProductData();
      } else {
        this.productData = this.searchProductData();
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
