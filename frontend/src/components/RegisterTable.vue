<template>
  <div class="form-container">
    <h1 class="page-title">基于NLP的可视化评价信息收集与分析系统</h1>
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
        <a-space>
          <a-button type="primary" class="register-button" @click="goToLogin">登录</a-button>
          <a-space style="width: 120px;"></a-space>
          <a-button type="primary" class="login-button" html-type="submit">注册</a-button>
        </a-space>
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
          const response = await axios.post("http://localhost:8080/register", this.registerData);
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
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
  border-radius: 10px;
}

.page-title {
  text-align: center;
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 40px;
  color: deepskyblue;
}

a-space {
  display: inline-block;
}

.login-button {
  background-color: #1890ff;
  border-color: #1890ff;
  margin-left: 50px;
}

.login-button:hover {
  background-color: #40a9ff;
  border-color: #40a9ff;
}

.register-button {
  background-color: #f5222d;
  border-color: #f5222d;
  margin-right: 50px;
}

.register-button:hover {
  background-color: #ff4d4f;
  border-color: #ff4d4f;
}
</style>