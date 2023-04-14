import { createRouter, createWebHashHistory } from 'vue-router'


import LoginTable from './components/LoginTable.vue'
import RegisterTable from './components/RegisterTable.vue'
import Home from './components/Home.vue'
import TaskList from "./components/tasks/TaskList.vue";
import RunWeiboTasks from "@/components/spider/weibo/RunWeiboTasks.vue";
import RunJDTasks from "@/components/spider/jd/RunJDTasks.vue";
import UserCenter from "@/components/UserCenter.vue";

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    component: LoginTable,
    meta: {
      public: true,
      title: "用户登录"
    }
  },
  {
    path: '/register',
    component: RegisterTable,
    meta: {
      public: true,
      title: "用户注册"
    }
  },
  {
    path: '/home',
    component: Home,
    meta: {
      title: "主页"
    }
  },
  {
    path: '/user_center',
    component: UserCenter
  },
  {
    path: '/weibo/run_tasks',
    component: RunWeiboTasks
  },
  {
    path: '/jd/run_tasks',
    component: RunJDTasks
  },
  {
    path: '/task_center',
    component: TaskList
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
