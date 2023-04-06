<template>
  <a-layout>
    <a-layout-sider>
      <a-menu :defaultSelectedKeys="['user']" :selectedKeys="[selectedTask]" @select="handleMenuSelect">
        <a-menu-item key="user">User Spider</a-menu-item>
        <a-menu-item key="search">Search Spider</a-menu-item>
        <a-menu-item key="fan">Fan Spider</a-menu-item>
        <a-menu-item key="tweet">Tweet Spider</a-menu-item>
        <a-menu-item key="follower">Follower Spider</a-menu-item>
        <a-menu-item key="comment">Comment Spider</a-menu-item>
        <a-menu-item key="repost">Repost Spider</a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout-content style="padding: 24px">
      <a-card>
        <a-form :model="userData"  v-if="selectedTask === 'user'"  @submit.prevent="submitUserSpider">
          <a-form-item label="User IDs" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="userData.user_ids" placeholder="Enter user IDs separated by comma" />
          </a-form-item>
          <a-form-item label="Cookie" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="userData.cookie" placeholder="Enter cookie" />
          </a-form-item>
          <a-form-item :wrapper-col="{ offset: 4 }">
            <a-button type="primary" html-type="submit">Submit</a-button>
          </a-form-item>
        </a-form>
        <a-form :model="searchData" v-else-if="selectedTask === 'search'"  @submit.prevent="submitSearchSpider">
          <a-form-item label="Keywords" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="searchData.keywords" placeholder="Enter keywords separated by comma" />
          </a-form-item>
          <a-form-item label="Start Time" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-date-picker
              v-model:value="searchData.startTime"
              show-time
              format="YYYY-MM-DD-HH"
              placeholder="Select start time"
            />
          </a-form-item>
          <a-form-item label="End Time" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-date-picker
              v-model:value="searchData.endTime"
              show-time
              format="YYYY-MM-DD-HH"
              placeholder="Select end time"
            />
          </a-form-item>

          <a-form-item label="Sort By Hot" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-switch v-model:checked="searchData.is_sort_by_hot" />
          </a-form-item>
          <a-form-item label="Specific Time Scope" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-switch v-model:checked="searchData.is_search_with_specific_time_scope" />
          </a-form-item>
          <a-form-item label="Cookie" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="searchData.cookie" placeholder="Enter cookie" />
          </a-form-item>
          <a-form-item :wrapper-col="{ offset: 4 }">
            <a-button type="primary" html-type="submit">Submit</a-button>
          </a-form-item>
        </a-form>
        <a-form :model="fanData" v-else-if="selectedTask === 'fan'" @submit.prevent="submitFanSpider">
          <a-form-item label="User IDs" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="fanData.user_ids" placeholder="Enter user IDs separated by comma" />
          </a-form-item>
          <a-form-item label="Cookie" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="fanData.cookie" placeholder="Enter cookie" />
          </a-form-item>
          <a-form-item :wrapper-col="{ offset: 4 }">
            <a-button type="primary" html-type="submit">Submit</a-button>
          </a-form-item>
        </a-form>

        <a-form :model="tweetData" v-else-if="selectedTask === 'tweet'" @submit.prevent="submitTweetSpider">
          <a-form-item label="User IDs" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="tweetData.user_ids" placeholder="Enter user IDs separated by comma" />
          </a-form-item>
          <a-form-item label="Cookie" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="tweetData.cookie" placeholder="Enter cookie" />
          </a-form-item>
          <a-form-item :wrapper-col="{ offset: 4 }">
            <a-button type="primary" html-type="submit">Submit</a-button>
          </a-form-item>
        </a-form>

        <a-form :model="followerData" v-else-if="selectedTask === 'follower'" @submit.prevent="submitFollowerSpider">
          <a-form-item label="User IDs" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="followerData.user_ids" placeholder="Enter user IDs separated by comma" />
          </a-form-item>
          <a-form-item label="Cookie" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="followerData.cookie" placeholder="Enter cookie" />
          </a-form-item>
          <a-form-item :wrapper-col="{ offset: 4 }">
            <a-button type="primary" html-type="submit">Submit</a-button>
          </a-form-item>
        </a-form>

        <a-form :model="commentData" v-else-if="selectedTask === 'comment'" @submit.prevent="submitCommentSpider">
          <a-form-item label="Tweet IDs" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="commentData.tweet_ids" placeholder="Enter tweet IDs separated by comma" />
          </a-form-item>
          <a-form-item label="Cookie" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="commentData.cookie" placeholder="Enter cookie" />
          </a-form-item>
          <a-form-item :wrapper-col="{ offset: 4 }">
            <a-button type="primary" html-type="submit">Submit</a-button>
          </a-form-item>
        </a-form>

        <a-form :form="repostData" v-else-if="selectedTask === 'repost'" @submit.prevent="submitRepostSpider">
          <a-form-item label="Tweet IDs" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="repostData.tweetIds" placeholder="Enter tweet IDs separated by comma" />
          </a-form-item>
          <a-form-item label="Cookie" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-input v-model:value="repostData.cookie" placeholder="Enter cookie" />
          </a-form-item>
          <a-form-item :wrapper-col="{ offset: 4 }">
            <a-button type="primary" html-type="submit">Submit</a-button>
          </a-form-item>
        </a-form>
      </a-card>
    </a-layout-content>
  </a-layout>
</template>

<script>
import { defineComponent } from 'vue'
import { Menu, Layout, Form, Input, Button, message, DatePicker, Switch, Card } from 'ant-design-vue'
import axiosInstance from "@/api/axiosInstance";
//import moment from 'moment';


export default defineComponent({
  name: 'RunTasks',
  components: {
    'a-menu': Menu,
    'a-menu-item': Menu.Item,
    'a-form': Form,
    'a-form-item': Form.Item,
    'a-input': Input,
    'a-button': Button,
    'a-layout': Layout,
    'a-layout-sider': Layout.Sider,
    'a-layout-content': Layout.Content,
    'a-switch': Switch,
    'a-card': Card,
    'a-date-picker': DatePicker
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
    }
  },
  methods: {
    handleMenuSelect({ key }) {
      this.selectedTask = key
    },
    submitUserSpider() {
        const formData = {
            user_ids: this.userData.user_ids.split(','),
            cookie: this.userData.cookie
        }
        console.log( JSON.stringify(formData))

        axiosInstance.post('/run_weibo_user_spider', JSON.stringify(formData), {
            headers: {
              'Content-Type': 'application/json',
            },
        }).then(response => {
            message.success('User spider task submitted successfully')
            console.log(response)
        })
        .catch(error => {
            message.error('Error submitting user spider task')
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
        axiosInstance.post('/run_weibo_search_spider', JSON.stringify(formData), {
            headers: {
              'Content-Type': 'application/json',
            },
        })
        .then(response => {
            message.success('Search spider task submitted successfully')
            console.log(response)
        })
        .catch(error => {
            message.error('Error submitting search spider task')
            console.log(error)
        })
    },
    submitFanSpider() {
        const formData = {
            user_ids: this.fanData.user_ids.split(','),
            cookie: this.fanData.cookie
        }
        axiosInstance.post('/run_weibo_fan_spider', JSON.stringify(formData), {
            headers: {
              'Content-Type': 'application/json',
            },
        })
        .then(response => {
            message.success('Fan spider task submitted successfully')
            console.log(response)
        })
        .catch(error => {
            message.error('Error submitting fan spider task')
            console.log(error)
        })
    },
    submitTweetSpider() {
        const formData = {
            user_ids: this.tweetData.user_ids.split(','),
            cookie: this.tweetData.cookie
        }
        axiosInstance.post('/run_weibo_tweet_spider', JSON.stringify(formData), {
            headers: {
              'Content-Type': 'application/json',
            },
        })
        .then(response => {
            message.success('Tweet spider task submitted successfully')
            console.log(response)
        })
        .catch(error => {
            message.error('Error submitting tweet spider task')
            console.log(error)
        })
    },
    submitFollowerSpider() {
        const formData = {
            user_ids: this.followerData.user_ids.split(','),
            cookie: this.followerData.cookie
        }
        axiosInstance.post('/run_weibo_follower_spider', JSON.stringify(formData), {
            headers: {
              'Content-Type': 'application/json',
            },
        })
        .then(response => {
            message.success('Follower spider task submitted successfully')
            console.log(response)
        })
        .catch(error => {
            message.error('Error submitting follower spider task')
            console.log(error)
        })
    },
    submitCommentSpider() {
        const formData = {
            tweet_ids: this.commentData.tweet_ids.split(','),
            cookie: this.commentData.cookie
        }
        axiosInstance.post('/run_weibo_comment_spider', JSON.stringify(formData), {
            headers: {
              'Content-Type': 'application/json',
            },
        })
        .then(response => {
            message.success('Comment spider task submitted successfully')
            console.log(response)
        })
        .catch(error => {
            message.error('Error submitting comment spider task')
            console.log(error)
        })
    },
    submitRepostSpider() {
      const formData = {
        tweet_ids: this.repostData.tweet_ids.split(','),
        cookie: this.repostData.cookie
      }
      axiosInstance.post('/run_weibo_repost_spider', JSON.stringify(formData), {
            headers: {
              'Content-Type': 'application/json',
            },
        })
      .then(response => {
        message.success('Repost spider task submitted successfully')
        console.log(response)
      })
      .catch(error => {
        message.error('Error submitting repost spider task')
        console.log(error)
      })
    }

  }
})
</script>



<style scoped>
a-menu {
  overflow-y: auto;
  max-height: calc(100vh - 64px); /* assuming your header has a height of 64px */
}


</style>
