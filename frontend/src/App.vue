<template>
  <div id="app">
    <router-view> </router-view>
  </div>
</template>

<script>

export default {
  name: 'App',
  components: {

  },
  created() {
    document.title = "基于NLP的可视化评价信息收集与分析系统"; // 设置整个App的title
  },
  data() {
    return {
      showLogin: false
    }
  },
  methods: {

  },
}
</script>
