<template>
  <div style="padding: 24px;">
    <h1>前后端联调测试</h1>
    <p>后端返回：{{ message }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  data() {
    return { message: "正在请求后端..." };
  },
  mounted() {
    axios
      .get("/api/hello/")
      .then((res) => (this.message = res.data.message))
      .catch((err) => (this.message = "请求失败：" + err));
  },
};
</script>
