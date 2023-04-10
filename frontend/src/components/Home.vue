<template>
  <div>
    <a-layout>
      <a-layout-header>
        <a-menu :default-selected-keys="['home']" mode="horizontal" @click="handleMenuClick">
          <a-menu-item key="home">Home</a-menu-item>
          <a-menu-item key="user_center">User Center</a-menu-item>
          <a-menu-item key="task_center">Task Center</a-menu-item>
          <a-menu-item key="weibo/run_tasks">Weibo Spider</a-menu-item>
          <a-menu-item key="data_analysis">Data Analysis</a-menu-item>
          <a-menu-item key="data_management">Data Management</a-menu-item>
        </a-menu>
      </a-layout-header>
      <a-layout-content style="padding: 24px">
        <router-view></router-view>
      </a-layout-content>
    </a-layout>
  </div>
</template>

<script>
export default {
  name: 'LayoutComponent',
  methods: {
    handleMenuClick({ key }) {
      this.$router.push(`/${key}`)
    }
  }
}
</script>

<style scoped>
/* add styles for the layout component */
</style>

<style scoped>

.ant-layout-header {
    height: 64px;
    padding: 0 50px;
    color: #ffffff;
    line-height: 64px;
    background: #fff;
}

h1 {
  text-align: center;
  margin-top: 50px;
}
ul {
  list-style-type: none;
  display: flex;
  justify-content: center;
  margin-top: 50px;
}
li {
  margin: 10px;
}
</style>
