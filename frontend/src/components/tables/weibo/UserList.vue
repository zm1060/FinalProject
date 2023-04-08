<template>
  <div class="user-list">
    <h2>User List</h2>
    <ul>
      <li v-for="user in userList" :key="user._id">
        <router-link :to="{ name: 'UserProfile', params: { id: user._id }}">
          <h3>{{ user.name }}</h3>
          <img :src="user.profile_image_url" :alt="user.name">
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'UserList',
  props: {
    userList: {
      type: Array,
      required: true
    }
  }
}
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
