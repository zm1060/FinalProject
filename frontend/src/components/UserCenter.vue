<template>
  <div>
    <a-layout style="min-height: 100vh">
      <a-layout-header>

        <a-menu mode="horizontal" theme="dark">
          <a-menu-item>
              <a-button type="primary" @click="$router.push('/home')">Back to Homepage</a-button>
          </a-menu-item>
          <a-menu-item>用户中心</a-menu-item>
        </a-menu>
      </a-layout-header>
      <a-layout-content style="padding: 0 50px">
        <a-breadcrumb style="margin: 16px 0">
          <a-breadcrumb-item>用户中心</a-breadcrumb-item>
          <a-breadcrumb-item>个人信息</a-breadcrumb-item>
        </a-breadcrumb>
        <a-form :model="userData" :label-col="{span: 4}" :wrapper-col="{span: 14}">
          <a-form-item label="用户名">
            <a-input v-model:value="userData.username"></a-input>
          </a-form-item>
          <a-form-item label="邮箱">
            <a-input v-model:value="userData.email"></a-input>
          </a-form-item>
          <a-form-item label="密码">
            <a-input type="password" v-model:value="userData.password"></a-input>
          </a-form-item>
          <a-form-item>
            <a-button class="update-button" type="primary" @click="updateUser">更新信息</a-button>
          </a-form-item>
          <a-form-item>
            <a-button class="delete-button" type="danger" @click="deleteUser">注销该账号</a-button>
          </a-form-item>
        </a-form>
      </a-layout-content>
    </a-layout>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import {Layout, Menu, Breadcrumb, Form, Input, Button, message} from 'ant-design-vue'
import axiosInstance from "@/api/axiosInstance";

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
        userData: {
          username: '',
          email: '',
          password: '',
        },

    }
  },
  methods: {
    async getUserInfo() {
      try {
        const response = await axiosInstance.get('/me')
        this.username = response.data.user_name
        this.email = response.data.email
        message.success("获取用户信息成功!")
      } catch (error) {
        console.error(error)
        message.error("获取用户信息失败!")
      }
    },
    async updateUser() {
      try {
        const data = {
          username: this.userData.username,
          email: this.userData.email,
          password: this.userData.password,
        }
        const response = await axiosInstance.put('/me', data)
        this.username = response.data.user_name
        this.email = response.data.email
        this.password = ''
        message.success("更新用户信息成功!")
        this.$router.push('/login')
      } catch (error) {
        console.error(error)
        message.error("更新用户信息失败!")
      }
    },
    async deleteUser() {
      try {
        await axiosInstance.delete('/me')
          this.$router.push('/login')
          message.success("删除用户成功!")
      } catch (error) {
          console.error(error)
          message.error("删除用户失败!")
      }
    },
  },
  mounted() {
    this.getUserInfo()
  },
})
</script>
