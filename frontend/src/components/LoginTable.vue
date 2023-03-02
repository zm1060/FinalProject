<template>
  <div class="form-container">
    <a-form @submit.prevent="login" :model="loginData">
      <a-form-item label="用户名" name="username" :rules="usernameRules">
        <a-input v-model:value="loginData.username" />
      </a-form-item>
      <a-form-item label="密码" name="password" :rules="passwordRules">
        <a-input type="password" v-model:value="loginData.password" />
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">登录</a-button>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" @click="goToRegister">注册</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginTable",
  data() {
    return {
      loginData: {
        username: "",
        password: "",
        email: "",
        grant_type: "",
        client_id: "",
        client_secret: ""
      },
      usernameRules: [
        { required: true, message: '请输入您的用户名', trigger: 'blur' }
      ],
      passwordRules: [
        { required: true, message: '请输入您的密码', trigger: 'blur' }
      ],
      isAuthenticated: false
    };
  },
    methods: {
      async login() {
        try {
          const response = await axios.post("http://localhost:8080/login", this.loginData, {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              'accept': 'application/json'
            }
          });
          const token = response.data.access_token
          // Store the token in local storage
          localStorage.setItem("access_token", token);
          // Set isAuthenticated to true
          this.isAuthenticated = true;
          // Set the Authorization header for subsequent requests
          axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`;
          alert("登录成功");
          this.$router.push('/home')
        } catch (error) {
          alert("登录失败：" + error.response.data.detail);
        }
      },
      goToRegister() {
        this.$router.push('/register')
      }
  },
}
</script>

<style scoped>
.form-container {
  background-image: url('../assets/bg7.jpg');
  background-size: cover;
  background-position: center;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>