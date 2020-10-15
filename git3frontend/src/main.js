import Vue from 'vue';
import App from './App.vue';
import store from './store';
import vuetify from './plugins/vuetify';

const Web3 = require('web3');

Vue.config.productionTip = false;

Vue.prototype.$web3 = new Web3();

new Vue({
  store,
  vuetify,
  theme: {
    dark: true,
  },
  render: (h) => h(App),
}).$mount('#app');
