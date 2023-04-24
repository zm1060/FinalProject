<template>
  <a-menu mode="horizontal">
      <a-menu-item>
        <a-button type="primary" @click="$router.push('/home')">回到主页</a-button>
      </a-menu-item>
      <a-menu-item>
        <a-button @click="$router.push('/task_center')">任务列表</a-button>
      </a-menu-item>
      <a-menu-item>
        <a-button @click="showData = !showData">数据展示</a-button>
      </a-menu-item>
      <a-menu-item>
        <a-button @click="$router.push('/help_center')">帮助中心</a-button>
      </a-menu-item>
      <a-menu-item>
        <a-button @click="$router.push('/login')">退出登录</a-button>
      </a-menu-item>
  </a-menu>
  <a-layout class="main-layout">
    <a-layout-sider class="sider">
      <a-menu :defaultSelectedKeys="['user']" :selectedKeys="[selectedTask]" @select="handleMenuSelect">
        <a-menu-item key="user">用户信息收集</a-menu-item>
        <a-menu-item key="search">关键字查询</a-menu-item>
        <a-menu-item key="fan">粉丝信息收集</a-menu-item>
        <a-menu-item key="tweet">博客信息收集</a-menu-item>
        <a-menu-item key="follower">关注者信息收集</a-menu-item>
        <a-menu-item key="comment">评论信息收集</a-menu-item>
        <a-menu-item key="repost">转发信息收集</a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout-content style="padding: 23px" class="content">
      <a-card>
        <a-form :model="userData"  v-if="selectedTask === 'user'"  @submit.prevent="submitUserSpider">
          <a-form-item label="User IDs" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="userData.user_ids" placeholder="输入用户ID," />
          </a-form-item>
          <a-form-item label="Cookie" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="userData.cookie" placeholder="输入Cookie" />
          </a-form-item>
          <a-form-item :wrapper-col="{ offset: 4 }">
            <a-button type="primary" html-type="submit">提交</a-button>
          </a-form-item>
        </a-form>
        <a-form :model="searchData" v-else-if="selectedTask === 'search'"  @submit.prevent="submitSearchSpider">
          <a-form-item label="Keywords" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="searchData.keywords" placeholder="输入关键字," />
          </a-form-item>
          <a-form-item label="Start Time" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-date-picker
              v-model:value="searchData.startTime"
              show-time
              format="YYYY-MM-DD-HH"
              placeholder="选择开始时间"
            />
          </a-form-item>
          <a-form-item label="End Time" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-date-picker
              v-model:value="searchData.endTime"
              show-time
              format="YYYY-MM-DD-HH"
              placeholder="选择结束时间"
            />
          </a-form-item>

          <a-form-item label="根据热度优先收集" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-switch v-model:checked="searchData.is_sort_by_hot" />
          </a-form-item>
          <a-form-item label="是否指定时间范围" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-switch v-model:checked="searchData.is_search_with_specific_time_scope" />
          </a-form-item>
          <a-form-item label="Cookie" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="searchData.cookie" placeholder="输入Cookie" />
          </a-form-item>
          <a-form-item :wrapper-col="{ offset: 4 }">
            <a-button type="primary" html-type="submit">提交</a-button>
          </a-form-item>
        </a-form>
        <a-form :model="fanData" v-else-if="selectedTask === 'fan'" @submit.prevent="submitFanSpider">
          <a-form-item label="User IDs" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="fanData.user_ids" placeholder="输入用户ID" />
          </a-form-item>
          <a-form-item label="Cookie" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="fanData.cookie" placeholder="输入Cookie" />
          </a-form-item>
          <a-form-item :wrapper-col="{ offset: 4 }">
            <a-button type="primary" html-type="submit">提交</a-button>
          </a-form-item>
        </a-form>

        <a-form :model="tweetData" v-else-if="selectedTask === 'tweet'" @submit.prevent="submitTweetSpider">
          <a-form-item label="User IDs" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="tweetData.user_ids" placeholder="输入用户ID" />
          </a-form-item>
          <a-form-item label="Cookie" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="tweetData.cookie" placeholder="输入Cookie" />
          </a-form-item>
          <a-form-item :wrapper-col="{ offset: 4 }">
            <a-button type="primary" html-type="submit">提交</a-button>
          </a-form-item>
        </a-form>

        <a-form :model="followerData" v-else-if="selectedTask === 'follower'" @submit.prevent="submitFollowerSpider">
          <a-form-item label="User IDs" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="followerData.user_ids" placeholder="输入用户ID" />
          </a-form-item>
          <a-form-item label="Cookie" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="followerData.cookie" placeholder="输入Cookie" />
          </a-form-item>
          <a-form-item :wrapper-col="{ offset: 4 }">
            <a-button type="primary" html-type="submit">提交</a-button>
          </a-form-item>
        </a-form>

        <a-form :model="commentData" v-else-if="selectedTask === 'comment'" @submit.prevent="submitCommentSpider">
          <a-form-item label="Tweet IDs" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="commentData.tweet_ids" placeholder="输入博客ID" />
          </a-form-item>
          <a-form-item label="Cookie" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="commentData.cookie" placeholder="输入Cookie" />
          </a-form-item>
          <a-form-item :wrapper-col="{ offset: 4 }">
            <a-button type="primary" html-type="submit">提交</a-button>
          </a-form-item>
        </a-form>

        <a-form :form="repostData" v-else-if="selectedTask === 'repost'" @submit.prevent="submitRepostSpider">
          <a-form-item label="Tweet IDs" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="repostData.tweet_ids" placeholder="输入博客ID" />
          </a-form-item>
          <a-form-item label="Cookie" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="repostData.cookie" placeholder="输入Cookie" />
          </a-form-item>
          <a-form-item :wrapper-col="{ offset: 4 }">
            <a-button type="primary" html-type="submit">提交</a-button>
          </a-form-item>
        </a-form>


      </a-card>
    <component v-if="showData === true" :is="Component"></component>

    </a-layout-content>
  </a-layout>
</template>

<script>
import { defineComponent } from 'vue'
import { Menu, Layout, Form, Input, Button, message, DatePicker, Switch, Card, Avatar } from 'ant-design-vue'
import axiosInstance from "@/api/axiosInstance";
import UserList from "@/components/tables/weibo/UserList.vue";
import SearchList from "@/components/tables/weibo/SearchList.vue";
import FanList from "@/components/tables/weibo/FanList.vue";
import TweetList from "@/components/tables/weibo/TweetList.vue";
import FollowerList from "@/components/tables/weibo/FollowerList.vue";
import CommentList from "@/components/tables/weibo/WeiboCommentList.vue";
import RepostList from "@/components/tables/weibo/RepostList.vue";

export default defineComponent({
  name: 'RunWeiboTasks',
  components: {
    'a-menu': Menu,
    'a-menu-item': Menu.Item,
    'a-form': Form,
    'a-form-item': Form.Item,
    'a-input': Input,
    'a-button': Button,
    'a-layout': Layout,
    'a-layout-sider': Layout.Sider,
    'a-layout-header': Layout.Header,
    'a-layout-content': Layout.Content,
    'a-switch': Switch,
    'a-card': Card,
    'a-date-picker': DatePicker,
    'a-avatar': Avatar,
  },
  data() {
    return {
        userData: {
            user_ids: '',
            cookie: ''
        },
        searchData: {
            keywords: '',
            start_time: '',
            end_time: '',
            is_sort_by_hot: true,
            is_search_with_specific_time_scope: false,
            cookie: ''
        },
        fanData: {
            user_ids: '',
            cookie: ''
        },
        tweetData: {
            user_ids: '',
            cookie: ''
        },
        followerData: {
            user_ids: '',
            cookie: ''
        },
        commentData: {
            tweet_ids: '',
            cookie: ''
        },
        formData: {
            tweet_ids: '',
            cookie: ''
        },
        repostData: {
          tweet_ids: '',
          cookie: ''
        },
        selectedTask: 'user', // default task type
        componentMap: {
          user: UserList,
          search: SearchList,
          fan: FanList,
          tweet: TweetList,
          follower: FollowerList,
          comment: CommentList,
          repost: RepostList,
        },
        showData: true,
        showTaskList: false,
    }
  },
  methods: {
    handleMenuSelect({ key }) {
      this.selectedTask = key;
      this.Component = this.componentMap[key];
    },
    submitUserSpider() {
        const formData = {
            user_ids: this.userData.user_ids.split(','),
            cookie: this.userData.cookie
        }
        console.log(JSON.stringify(formData))
        message.loading('正在加载用户爬虫任务！', 0.2)
        axiosInstance.post('/weibo/run_weibo_user_spider', JSON.stringify(formData), {
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(response => {
            message.success('用户爬虫任务提交成功！')
            console.log(response)
        })
            .catch(error => {
                message.error('提交用户爬虫任务时出错！')
                console.log(error)
            })
    },
    submitSearchSpider() {
        // format the datetime strings to the desired format
        //const formatted_start_time = moment(this.searchData.start_time).format('YYYY-MM-DD-HH');
        //const formatted_end_time = moment(this.searchData.end_time).format('YYYY-MM-DD-HH');
        const formData = {
            keywords: this.searchData.keywords.split(','),
            start_time: this.searchData.start_time,
            end_time: this.searchData.end_time,
            is_sort_by_hot: this.searchData.is_sort_by_hot,
            is_search_with_specific_time_scope: this.searchData.is_search_with_specific_time_scope,
            cookie: this.searchData.cookie
        }
        console.log(JSON.stringify(formData))
        axiosInstance.post('/weibo/run_weibo_search_spider', JSON.stringify(formData), {
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => {
                message.success('搜索爬虫任务提交成功！')
                console.log(response)
            })
            .catch(error => {
                message.error('提交搜索爬虫任务时出错！')
                console.log(error)
            })
    },
    submitFanSpider() {
        const formData = {
            user_ids: this.fanData.user_ids.split(','),
            cookie: this.fanData.cookie
        }
        axiosInstance.post('/weibo/run_weibo_fan_spider', JSON.stringify(formData), {
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => {
                message.success('粉丝爬虫任务提交成功！')
                console.log(response)
            })
            .catch(error => {
                message.error('提交粉丝爬虫任务时出错！')
                console.log(error)
            })
    },
    submitTweetSpider() {
        const formData = {
            user_ids: this.tweetData.user_ids.split(','),
            cookie: this.tweetData.cookie
        }
        axiosInstance.post('/weibo/run_weibo_tweet_spider', JSON.stringify(formData), {
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => {
                message.success('微博爬虫任务提交成功！')
                console.log(response)
            })
            .catch(error => {
                message.error('提交微博爬虫任务时出错！')
                console.log(error)
            })
    },
    submitFollowerSpider() {
        const formData = {
            user_ids: this.followerData.user_ids.split(','),
            cookie: this.followerData.cookie
        }
        axiosInstance.post('/weibo/run_weibo_follower_spider', JSON.stringify(formData), {
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            message.success('粉丝爬虫任务已成功提交')
            console.log(response)
        })
        .catch(error => {
            message.error('提交粉丝爬虫任务时出错')
            console.log(error)
        })
    },
    submitCommentSpider() {
        const formData = {
            tweet_ids: this.commentData.tweet_ids.split(','),
            cookie: this.commentData.cookie
        }
        axiosInstance.post('/weibo/run_weibo_comment_spider', JSON.stringify(formData), {
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            message.success('评论爬虫任务已成功提交')
            console.log(response)
        })
        .catch(error => {
            message.error('提交评论爬虫任务时出错')
            console.log(error)
        })
    },

    submitRepostSpider() {
        const formData = {
            tweet_ids: this.repostData.tweet_ids.split(','),
            cookie: this.repostData.cookie
        }
        axiosInstance.post('/weibo/run_weibo_repost_spider', JSON.stringify(formData), {
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            message.success('转发爬虫任务已成功提交')
            console.log(response)
        })
        .catch(error => {
            message.error('提交转发爬虫任务时出错')
            console.log(error)
        })
    }


  }
})
</script>



<style scoped>
/* General Layout */
.main-layout {
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Sider */
.sider {
  background-color: #f0f2f5;
}

.sider a {
  color: #f0f2f5;
}

/* Menu */
.main-layout .ant-menu {
  background-color: #f0f2f5;
  border-right: none;
}

.main-layout .ant-menu-item {
  height: 48px;
  line-height: 48px;
  font-size: 16px;
}

.main-layout .ant-menu-item-selected {
  background-color: #4544ff;
}

/* Header */
.main-layout .ant-layout-header {
  background-color: #f0f2f5;
  padding: 0;
  height: auto;
}

/* Content */
.content {
  background-color: #f0f2f5;
}

/* Card */
.a-card {
  background-color: #fff;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* Form */
.a-form-item {
  margin-bottom: 16px;
}

.a-form-item label {
  font-weight: 500;
}

/* Buttons */
.a-button {
  font-weight: 500;
}

</style>
