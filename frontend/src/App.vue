<template>
  <div>
    <LoginForm @login-success="handleLoginSuccess" />
  </div>
</template>

<script>
import axios from 'axios';
import LoginForm from './components/LoginForm.vue';


export default {
  name: 'App',
  components: {
    LoginForm
  },
  data() {
    return {
      isAuthenticated: false,
    };
  },
  methods: {
    async handleLoginSuccess(token) {
      // Store the token in local storage
      localStorage.setItem('access_token', token);

      // Set isAuthenticated to true
      this.isAuthenticated = true;

      // Set the Authorization header for subsequent requests
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    },
    logout() {
      // Remove the token from local storage
      localStorage.removeItem('access_token');

      // Set isAuthenticated to false
      this.isAuthenticated = false;

      // Remove the Authorization header for subsequent requests
      delete axios.defaults.headers.common['Authorization'];
    },
  },
};
</script>