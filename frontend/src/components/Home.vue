<template>
  <div>
    <h1>Welcome to Weibo Spider App</h1>
    <ul>
      <li><router-link to="/weibo/run_tasks">Go to Weibo Spider Page</router-link></li>
      <li><router-link to="/weibo/analy">Go to Weibo Spider Data Analy Page</router-link></li>
      <li><router-link to="/show">Go to Weibo Spider Data Show Page</router-link></li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "HomePage"
}
</script>

<style scoped>
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
