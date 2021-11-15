<template>
  <div class="Testing">
    <input type="button" value="submit" @click="onLoad()">
    <p>{{this.info}}</p>
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
    onLoad() {

      const axios = require('axios').default;
      const apiKey = 'a5y3ft5z9a2ejvcym8zkh3xe'

      axios({
        method: 'get',
        url: `https://api.sportradar.com/rugby-union/trial/v3/en/compeitions.json?api_key=${apiKey}`,
        headers: {
          'Access-Control-Allow-Origin': '*',
      }
      })
      .then(res => (this.info = res))
      .catch(err => console.error(err));
    }
  }
}
</script>
