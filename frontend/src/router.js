import { createRouter, createWebHashHistory } from 'vue-router'


import LoginTable from './components/LoginTable.vue'
import RegisterTable from './components/RegisterTable.vue'
import Home from './components/Home.vue'
import RunTasks from "./components/spider/weibo/RunTasks.vue";

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    component: LoginTable
  },
  {
    path: '/register',
    component: RegisterTable
  },
  {
    path: '/home',
    component: Home
  },
  {
    path: '/weibo/run_tasks',
    component: RunTasks
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  if (to.path !== '/login' && to.path !== '/register' && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
