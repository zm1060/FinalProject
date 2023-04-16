<template>

  <div class="form-container">
    <h1 class="page-title">基于NLP的可视化评价信息收集与分析系统</h1>
    <a-form @submit.prevent="login" :model="loginData">
      <a-form-item label="用户名" name="username" :rules="usernameRules">
        <a-input v-model:value="loginData.username" />
      </a-form-item>
      <a-form-item label="密码" name="password" :rules="passwordRules">
        <a-input type="password" v-model:value="loginData.password" />
      </a-form-item>
      <a-from-item>
        <a-space>
          <a-button class="register-button" type="primary" @click="goToRegister">注册</a-button>
          <a-space style="width: 120px;"></a-space>
          <a-button class="login-button" type="primary" html-type="submit">登录</a-button>
        </a-space>
      </a-from-item>
    </a-form>
  </div>
</template>
<script>
import axiosInstance, {setAuthToken} from "@/api/axiosInstance";

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
        const response = await axiosInstance.post("/login", this.loginData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'accept': 'application/json'
          }
        });
        const token = response.data.access_token
        // Store the token in local storage
        localStorage.setItem("access_token", token);
        localStorage.setItem("username", this.loginData.username)
        // Set isAuthenticated to true
        this.isAuthenticated = true;
        // Set the Authorization header for subsequent requests
        setAuthToken(response.data.access_token);
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

a-form-item {
  margin-bottom: 20px;
}

a-input,
a-select,
a-radio-group,
a-checkbox-group {
  font-size: 16px;
  padding: 10px 12px;
}

a-form-item label {
  font-size: 16px;
  font-weight: bold;
}

a-button[type="primary"] {
  width: 100%;
  font-size: 16px;
  padding: 10px 0;
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