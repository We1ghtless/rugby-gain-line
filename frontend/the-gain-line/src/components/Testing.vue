<template>
  <div class="Testing">
    <input type="button" value="submit" @click="getComps()">
    <p v-for="item in this.info.data" :key="item.id">{{item}}</p>
  </div>
</template>

<script>
export default {
  name: 'Testing',
  data() {
    return {
      info: null
    }
  },
  methods: {
    getComps() {
      const axios = require('axios').default;

      axios({
        method: 'get',
        url: `http://127.0.0.1:5000/`
      })
      .then(res => (this.info = res))
      .catch(err => console.error(err));
    }
  }
}
</script>
