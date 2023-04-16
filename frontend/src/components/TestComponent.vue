<template>
  <div>
    <CommentCharts :comment="commentData" />
  </div>
</template>

<script>
import CommentCharts from "@/components/charts/Comment.vue";

export default {
  name: "TestComponent",
  components: {
    CommentCharts
  },
  data() {
    return {
      commentData: {
        "_id": {
          "$numberLong": "4891165990847758"
        },
        "created_at": "2023-04-16 14:58:28",
        "like_counts": 0,
        "ip_location": "来自湖北",
        "content": "跑的咋样？",
        "comment_user": {
          "_id": "1465232835",
          "avatar_hd": "https://tva2.sinaimg.cn/crop.0.0.180.180.1024/5755adc3jw1e8qgp5bmzyj2050050aa8.jpg?KID=imgbed,tva&Expires=1681663324&ssig=%2FULUgjCiW3",
          "nick_name": "香脆油墩子",
          "verified": true,
          "description": "我在减肥。。。",
          "followers_count": 794,
          "friends_count": 1642,
          "statuses_count": 4217,
          "gender": "m",
          "location": "上海 浦东新区",
          "mbrank": 1,
          "mbtype": 2,
          "verified_type": 0,
          "verified_reason": "青岛威达国际货运代理有限公司上海分公司 物流专员"
        },
        "crawl_time": 1681652524
      }
    };
  }
};
</script>
