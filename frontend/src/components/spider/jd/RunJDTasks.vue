<template>
  <a-menu mode="horizontal">
      <a-menu-item>
        <a-button type="primary" @click="$router.push('/home')">回到主页</a-button>
      </a-menu-item>
      <a-menu-item>
        <a-button @click="$router.push('/task_center')">任务列表</a-button>
      </a-menu-item>
      <a-menu-item>
        <a-button @click="showData = !showData">数据展示</a-button>
      </a-menu-item>
      <a-menu-item>
        <a-button @click="$router.push('/help_center')">帮助中心</a-button>
      </a-menu-item>
      <a-menu-item>
        <a-button @click="$router.push('/login')">退出登录</a-button>
      </a-menu-item>
  </a-menu>
  <a-layout class="main-layout">
    <a-layout-sider class="sider">
      <a-menu :defaultSelectedKeys="['product']" :selectedKeys="[selectedTask]" @select="handleMenuSelect">
        <a-menu-item key="product">产品信息收集</a-menu-item>
        <a-menu-item key="comment">评价信息收集</a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout-content style="padding: 23px" class="content">
      <a-card>
        <a-form :model="productData"  v-if="selectedTask === 'product'"  @submit.prevent="submitProductSpider">
          <a-form-item label="搜索名称" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="productData.search_name" placeholder="输入产品名称" />
          </a-form-item>
          <a-form-item :wrapper-col="{ offset: 4 }">
            <a-button type="primary" html-type="submit">提交</a-button>
          </a-form-item>
        </a-form>
        <a-form :model="commentData" v-else-if="selectedTask === 'comment'"  @submit.prevent="submitCommentSpider">
          <a-form-item label="产品链接" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="commentData.urls" placeholder="格式:https://item.jd.com/10067835733136.html" />
          </a-form-item>
          <a-form-item label="爬取页数" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="commentData.pages" placeholder="10"/>
          </a-form-item>
          <a-form-item :wrapper-col="{ offset: 4 }">
            <a-button type="primary" html-type="submit">提交</a-button>
          </a-form-item>
        </a-form>
      </a-card>
    <component v-if="showData === true" :is="Component"></component>

    </a-layout-content>
  </a-layout>
</template>

<script>
import { defineComponent } from 'vue'
import { Menu, Layout, Form, Input, Button, message, DatePicker, Card, Avatar } from 'ant-design-vue'
import axiosInstance from "@/api/axiosInstance";
import ProductList from "@/components/tables/jd/ProductList.vue";
import CommentList from "@/components/tables/jd/JDCommentList.vue";


export default defineComponent({
  name: 'RunJDTasks',
  components: {
    'a-menu': Menu,
    'a-menu-item': Menu.Item,
    'a-form': Form,
    'a-form-item': Form.Item,
    'a-input': Input,
    'a-button': Button,
    'a-layout': Layout,
    'a-layout-sider': Layout.Sider,
    'a-layout-header': Layout.Header,
    'a-layout-content': Layout.Content,
    'a-card': Card,
    'a-date-picker': DatePicker,
    'a-avatar': Avatar,
  },
  data() {
    return {
        productData: {
            search_name: '',
        },
        commentData: {
            urls: '',
            pages: '',
        },
        selectedTask: 'product', // default task type
        componentMap: {
          product: ProductList,
          comment: CommentList,
        },
        showData: true,
        showTaskList: false,
    }
  },
  methods: {
    handleMenuSelect({ key }) {
      this.selectedTask = key;
      this.Component = this.componentMap[key];
    },
    submitProductSpider() {
        const formData = {
            search_name: this.productData.search_name,
        }
        console.log( JSON.stringify(formData))
        message.loading('JD product spider task is Loading!',0.2)
        axiosInstance.post('/jd/run_jd_product_spider', JSON.stringify(formData), {
            headers: {
              'Content-Type': 'application/json',
            },
        }).then(response => {
            message.success('产品信息收集任务成功提交!')
            console.log(response)
        })
        .catch(error => {
            message.error('产品信息收集任务提交失败!')
            console.log(error)
        })
    },
    submitCommentSpider() {
        const formData = {
            urls: this.commentData.urls.split(','),
            pages: this.commentData.pages
        }
        axiosInstance.post('/jd/run_jd_comment_spider', JSON.stringify(formData), {
            headers: {
              'Content-Type': 'application/json',
            },
        })
        .then(response => {
            message.success('评价信息收集任务成功提交!')
            console.log(response)
        })
        .catch(error => {
            message.error('评价信息收集任务提交失败!')
            console.log(error)
        })
    },

  }
})
</script>



<style scoped>
/* General Layout */
.main-layout {
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Sider */
.sider {
  background-color: #f0f2f5;
}

.sider a {
  color: #f0f2f5;
}

/* Menu */
.main-layout .ant-menu {
  background-color: #f0f2f5;
  border-right: none;
}

.main-layout .ant-menu-item {
  height: 48px;
  line-height: 48px;
  font-size: 16px;
}

.main-layout .ant-menu-item-selected {
  background-color: #4544ff;
}

/* Header */
.main-layout .ant-layout-header {
  background-color: #f0f2f5;
  padding: 0;
  height: auto;
}

/* Content */
.content {
  background-color: #f0f2f5;
}

/* Card */
.a-card {
  background-color: #fff;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* Form */
.a-form-item {
  margin-bottom: 16px;
}

.a-form-item label {
  font-weight: 500;
}

/* Buttons */
.a-button {
  font-weight: 500;
}

</style>
