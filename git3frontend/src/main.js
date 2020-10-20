import Vue from 'vue';
import App from './App.vue';
import store from './store';
import vuetify from './plugins/vuetify';

const Web3 = require('web3');
const web3Config = require('./lib/web3Config.js');

Vue.config.productionTip = false;
Vue.prototype.$web3 = new Web3();
Vue.prototype.$web3Goerli = new Web3(new Web3.providers.HttpProvider(web3Config.GOERLI_RPC));
Vue.prototype.$web3Matic = new Web3(new Web3.providers.HttpProvider(web3Config.MATIC_RPC));

Vue.prototype.$web3Goerli.eth.ens.getAddress(web3Config.FACTORY_ENS_NAME).then((address) => {
  Vue.prototype.$factoryContract = new Vue.prototype.$web3Matic.eth.Contract(
    web3Config.GIT_FACTORY_INTERFACE, address,
  );
  console.log('Factory loaded');
});

new Vue({
  store,
  vuetify,
  theme: {
    dark: true,
  },
  render: (h) => h(App),
}).$mount('#app');
