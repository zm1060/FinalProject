<template>
  <div>
    <a-layout style="min-height: 100vh">
      <a-layout-header>
        <a-menu mode="horizontal" theme="dark">
          <a-menu-item>用户中心</a-menu-item>
        </a-menu>
      </a-layout-header>
      <a-layout-content style="padding: 0 50px">
        <a-breadcrumb style="margin: 16px 0">
          <a-breadcrumb-item>用户中心</a-breadcrumb-item>
          <a-breadcrumb-item>个人信息</a-breadcrumb-item>
        </a-breadcrumb>
        <a-form :model="{}" :label-col="{span: 4}" :wrapper-col="{span: 14}">
          <a-form-item label="用户名">
            <a-input v-model="username"></a-input>
          </a-form-item>
          <a-form-item label="邮箱">
            <a-input v-model="email"></a-input>
          </a-form-item>
          <a-form-item label="密码">
            <a-input type="password" v-model="password"></a-input>
          </a-form-item>
          <a-form-item>
            <a-button type="primary" @click="updateUser">更新信息</a-button>
          </a-form-item>
        </a-form>
        <a-button type="danger" @click="deleteUser">删除用户</a-button>
      </a-layout-content>
    </a-layout>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { Layout, Menu, Breadcrumb, Form, Input, Button } from 'ant-design-vue'
import axios from 'axios'

export default defineComponent({
  name: 'UserCenter',
  components: {
    'a-layout': Layout,
    'a-menu': Menu,
    'a-breadcrumb': Breadcrumb,
    'a-form': Form,
    'a-input': Input,
    'a-button': Button,
  },
  data() {
    return {
      username: '',
      email: '',
      password: '',
    }
  },
  methods: {
    async getUserInfo() {
      try {
        const response = await axios.get('/me')
        this.username = response.data.username
        this.email = response.data.email
      } catch (error) {
        console.error(error)
      }
    },
    async updateUser() {
      try {
        const data = {
          new_username: this.username,
          new_email: this.email,
          new_password: this.password,
        }
        const response = await axios.put('/me', data)
        this.username = response.data.username
        this.email = response.data.email
        this.password = ''
      } catch (error) {
        console.error(error)
      }
    },
    async deleteUser() {
      try {
        await axios.delete('/me')
        // Redirect to login page or display a message
      } catch (error) {
        console.error(error)
      }
    },
  },
  mounted() {
    this.getUserInfo()
  },
})
</script>
