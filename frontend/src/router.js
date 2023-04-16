import { createRouter, createWebHashHistory } from 'vue-router'


import LoginTable from './components/LoginTable.vue'
import RegisterTable from './components/RegisterTable.vue'
import Home from './components/Home.vue'
import TaskList from "./components/tasks/TaskList.vue";
import RunWeiboTasks from "@/components/spider/weibo/RunWeiboTasks.vue";
import RunJDTasks from "@/components/spider/jd/RunJDTasks.vue";
import UserCenter from "@/components/UserCenter.vue";
import WeiboCommentList from "@/components/tables/weibo/WeiboCommentList.vue";
import UserList from "@/components/tables/weibo/UserList.vue";
import TweetList from "@/components/tables/weibo/TweetList.vue";
import SearchList from "@/components/tables/weibo/SearchList.vue";
import RepostList from "@/components/tables/weibo/RepostList.vue";
import FollowerList from "@/components/tables/weibo/FollowerList.vue";
import FanList from "@/components/tables/weibo/FanList.vue";
import ProductList from "@/components/tables/jd/ProductList.vue";
import JDCommentList from "@/components/tables/jd/JDCommentList.vue";
import TestComponent from "@/components/TestComponent.vue";

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
    path: '/data_analysis',
    component: TestComponent
  },
  {
    path: '/data_management',
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
  },
  {
    path: '/weibo_comment_list/:taskId',
    name: 'weibo_comment_list',
    component: WeiboCommentList,
  },
  {
    path: '/weibo_user_list/:taskId',
    name: 'weibo_user_list',
    component: UserList,
  },
  {
    path: '/weibo_tweet_list/:taskId',
    name: 'weibo_tweet_list',
    component: TweetList,
  },
  {
    path: '/weibo_search_list/:taskId',
    name: 'weibo_search_list',
    component: SearchList,
  },
  {
    path: '/weibo_repost_list/:taskId',
    name: 'weibo_repost_list',
    component: RepostList,
  },
  {
    path: '/weibo_follower_list/:taskId',
    name: 'weibo_follower_list',
    component: FollowerList,
  },
  {
    path: '/weibo_fan_list/:taskId',
    name: 'weibo_fan_list',
    component: FanList,
  },
  {
    path: '/jd_product_list/:taskId',
    name: 'jd_product_list',
    component: ProductList,
  },
  {
    path: '/jd_comment_list/:taskId',
    name: 'jd_comment_list',
    component: JDCommentList,
  },
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
