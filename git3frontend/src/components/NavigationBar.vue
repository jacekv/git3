<template>
  <v-app-bar app>
    <img style='widht: 50px; height: 50px' src="@/assets/myLogo.png">
    <v-text-field
      class='pl-6 shrink'
      hide-details
      prepend-icon="mdi-magnify"
      single-line
      label="Search repository"
      @keydown.enter="searchFunction"
      v-model='search'
    ></v-text-field>
    <v-spacer/>
    <v-btn rounded @click='connectMetaMask'>
      {{ buttonText }}
    </v-btn>
  </v-app-bar>
</template>

<script>
import store from '../store/index';

const Web3 = require('web3');
const Contract = require('web3-eth-contract');
const web3Config = require('../lib/web3Config.js');

// // set provider for all later instances to use
Contract.setProvider(web3Config.RPC_ADDRESS);

const gitFactory = new Contract(web3Config.GIT_FACTORY_INTERFACE, web3Config.GIT_FACTORY_ADDRESS);

export default {
  name: 'NavigationBar',
  data() {
    return {
      search: '',
      buttonText: 'Connect to MetaMask',
    };
  },
  methods: {
    searchFunction() {
      gitFactory.methods.gitRepositories(this.search).call()
        .then((address) => {
          const repoContract = new Contract(web3Config.REPOSITORY_INTERFACE, address);
          return repoContract.methods.headCid().call();
        })
        .then(async (headCid) => {
          const response = await fetch(
            `${web3Config.IPFS_ADDRESS}/api/v0/file/ls?arg=${headCid}`,
            {
              method: 'POST',
            },
          );
          const data = await response.json();
          const files = [];
          data.Objects[headCid].Links.forEach((entry) => {
            files.push({
              name: entry.Name,
              type: entry.Type,
            });
          });
          store.commit('updateFileList', files);
          store.commit('updateRepoName', this.search);
          store.commit('toggleCode');
          store.commit('toggleLogo');
        });
    },
    async connectMetaMask() {
      let accounts = [];
      try {
        accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
      } catch (e) {
        console.log('User rejects MetaMask connection');
      }
      if (accounts.length === 0) return;
      store.commit('updateMetaMaskConnectionStatus', true);
      [this.buttonText] = accounts;
      this.buttonText = `${this.buttonText.substring(0, 6)}..${this.buttonText.substring(37)}`;
      const { networkVersion } = window.ethereum;

      this.$web3Goerli = new Web3(new Web3.providers.HttpProvider(web3Config.GOERLI_RPC));
      this.$web3Matic = new Web3(new Web3.providers.HttpProvider(web3Config.MATIC_RPC));
      this.$web3Goerli.eth.ens.getAddress(web3Config.FACTORY_ENS_NAME).then((address) => {
        console.log('Resolved address', address);
        this.$factoryContract.options.address = address;
      });

      if (networkVersion === '80001') {
        this.$web3.setProvider(new Web3.providers.HttpProvider(web3Config.MATIC_RPC));
      } else if (networkVersion === '5') {
        this.$web3.setProvider(new Web3.providers.HttpProvider(web3Config.GOERLI_RPC));
      }
      window.ethereum.on('chainChanged', (_chainId) => {
        // handler when the user changes the network
        if (_chainId === '0x13881') {
          this.$web3.setProvider(new Web3.providers.HttpProvider(web3Config.MATIC_RPC));
        } else if (_chainId === '0x5') {
          this.$web3.setProvider(new Web3.providers.HttpProvider(web3Config.GOERLI_RPC));
        }
      });
    },
  },
};
</script>
