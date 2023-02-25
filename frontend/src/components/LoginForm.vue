<template>
  <div>
    <div>
      <h1>登录</h1>
      <form>
        <label>
          用户名：
          <input type="text" v-model="loginData.username">
        </label>
        <br>
        <label>
          密码：
          <input type="password" v-model="loginData.password">
        </label>
        <br>
        <button type="submit" @click.prevent="login">登录</button>
      </form>
    </div>


    <div>
      <h1>注册</h1>
      <form>
        <label>
          用户名：
          <input type="text" v-model="registerData.username">
        </label>
        <br>
        <label>
          邮箱：
          <input type="text" v-model="registerData.email">
        </label>
        <br>
        <label>
          密码：
          <input type="password" v-model="registerData.password">
        </label>
        <br>
        <button type="submit" @click.prevent="register">注册</button>
      </form>
    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginForm",
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
      registerData: {
        username: "",
        password: "",
        email: "",
        grant_type: "",
        client_id: "",
        client_secret: ""
      },
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("http://127.0.0.1:8000/login", this.loginData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'accept': 'application/json'
          }
        });
        localStorage.setItem("access_token", response.data.access_token);
        alert("登录成功");
        this.$router.push('/dashboard');
      } catch (error) {
        alert("登录失败：" + error.response.data.detail);
        this.$router.push('/login');
      }
    },
    async register() {
      try {
        // eslint-disable-next-line no-unused-vars
        const response = await axios.post("http://127.0.0.1:8000/register", this.registerData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'accept': 'application/json'
          }
        });
        console.log(response)
        this.$router.push('/login');
      } catch (error) {
        alert("注册失败：" + error.response.data.detail);
      }
    },
  },
};
</script>


