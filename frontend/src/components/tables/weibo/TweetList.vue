<template>
  <div>
    <a-input v-model="taskId" placeholder="Enter Task ID" @pressEnter="getUserData" />
    <a-card v-if="userData._id" title="User Info">
      <a-avatar :src="userData.avatar_hd" />
      <p>{{ userData.nick_name }}</p>
      <p>{{ userData.verified_reason }}</p>
      <p>{{ userData.description }}</p>
      <p>{{ userData.location }}</p>
      <p>{{ userData.gender }}</p>
      <p>{{ userData.birthday }}</p>
      <p>{{ userData.followers_count }}</p>
      <p>{{ userData.friends_count }}</p>
      <p>{{ userData.statuses_count }}</p>
      <p>{{ userData.mbrank }}</p>
      <p>{{ userData.mbtype }}</p>
      <p>{{ userData.verified }}</p>
      <p>{{ userData.verified_type }}</p>
      <p>{{ userData.desc_text }}</p>
      <p>{{ userData.ip_location }}</p>
      <p>{{ userData.sunshine_credit }}</p>
      <div v-for="(label, index) in userData.label_desc" :key="index">
        <p>{{ label }}</p>
      </div>
    </a-card>
  </div>
</template>

<script>
import { ACard, AAvatar, AInput } from 'ant-design-vue';
import axios from 'axios';

export default {
  name: 'TweetList',
  components: {
    ACard,
    AAvatar,
    AInput,
  },
  data() {
    return {
      taskId: '',
      userData: {},
    };
  },
  methods: {
    getUserData() {
      axios.get(`http://localhost:8080/weibo/data/users?task_id=${this.taskId}`).then((response) => {
        this.userData = response.data[0];
      });
    },
  },
};
</script>


<style>
.user-list {
  margin: 20px;
}

ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

li {
  margin-bottom: 20px;
}

h3 {
  margin: 0;
}
</style>
