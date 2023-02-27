<template>
  <div class="form-container">
    <a-form @submit.prevent="register" :model="registerData">
      <a-form-item label="用户名" name="username" :rules="usernameRules">
        <a-input v-model:value="registerData.username" />
      </a-form-item>
      <a-form-item label="邮箱" name="email" :rules="emailRules">
        <a-input v-model:value="registerData.email" />
      </a-form-item>
      <a-form-item label="密码" name="password" :rules="passwordRules">
        <a-input type="password" v-model:value="registerData.password" />
      </a-form-item>
      <a-form-item>
        <a-button type="primary" @click="goToLogin">登录</a-button>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">注册</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "RegisterTable",
  data() {
    return {
      registerData: {
        username: "",
        password: "",
        email: ""
      },
      usernameRules: [
        { required: true, message: '请输入您的用户名', trigger: 'blur' }
      ],
      emailRules: [
        { required: true, message: '请输入您的邮箱', trigger: 'blur' }
      ],
      passwordRules: [
        { required: true, message: '请输入您的密码', trigger: 'blur' }
      ]
    };
  },
    methods: {
      async register() {
        try {
          // eslint-disable-next-line no-unused-vars
          const response = await axios.post("http://127.0.0.1:8000/register", this.registerData);
          console.log(response)
          alert("注册成功：" + this.registerData.username);
          this.$router.push('/login')
        } catch (error) {
          alert("注册失败：" + error.response.data.detail);
        }
      },
      goToLogin() {
        this.$router.push('/login')
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