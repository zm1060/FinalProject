<template>
  <div class="comment">
    <div class="comment-user">
      <img class="comment-user-avatar" :src="comment.comment_user.avatar_hd" :alt="comment.comment_user.nick_name">
      <div class="comment-user-info">
        <span class="comment-user-nick">{{ comment.comment_user.nick_name }}</span>
        <span class="comment-user-desc">{{ comment.comment_user.description }}</span>
      </div>
    </div>
    <div class="comment-content">{{ comment.content }}</div>
  </div>
</template>

<script>
export default {
  name: 'CommentCharts',
  props: {
    comment: {
      type: Object,
      required: true
    }
  }
};
</script>

<style>
.comment {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
}

.comment-user {
  display: flex;
  align-items: center;
}

.comment-user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}

.comment-user-nick {
  font-weight: bold;
}

.comment-user-desc {
  margin-left: 10px;
  color: #666;
}
</style>
