import Vue from 'vue';
import App from './App.vue';
import store from './store';
import vuetify from './plugins/vuetify';

const Web3 = require('web3');
const Contract = require('web3-eth-contract');
const web3Config = require('./lib/web3Config.js');

Vue.config.productionTip = false;

Vue.prototype.$web3 = new Web3();
Vue.prototype.$web3Goerli = new Web3();
Vue.prototype.$web3Matic = new Web3();
Vue.prototype.$factoryContract = new Contract(
  web3Config.GIT_FACTORY_INTERFACE, web3Config.GIT_FACTORY_ADDRESS,
);

new Vue({
  store,
  vuetify,
  theme: {
    dark: true,
  },
  render: (h) => h(App),
}).$mount('#app');
