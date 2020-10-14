<template>
  <v-app-bar app>
    <v-toolbar-title>Git3</v-toolbar-title>
    <v-text-field
      class='pl-6 shrink'
      hide-details
      prepend-icon="mdi-magnify"
      single-line
      label="Search repository"
      @keydown.enter="searchFunction"
      v-model='search'
    ></v-text-field>
  </v-app-bar>
</template>

<script>
import store from '../store/index';

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
    };
  },
  methods: {
    searchFunction() {
      gitFactory.methods.gitRepositories(this.search).call()
        .then((address) => {
          console.log('Address of repo', address);
          const repoContract = new Contract(web3Config.REPOSITORY_INTERFACE, address);
          return repoContract.methods.headCid().call();
        })
        .then(async (headCid) => {
          console.log('HeadCid', headCid);
          const response = await fetch(
            `http://127.0.0.1:5001/api/v0/file/ls?arg=${headCid}`,
            {
              method: 'POST',
            },
          );
          const data = await response.json();
          const files = [];
          data.Objects[headCid].Links.forEach((entry) => {
            console.log(entry.Name);
            files.push({
              name: entry.Name,
              type: entry.Type,
            });
          });
          store.commit('updateFileList', files);
          store.commit('updateRepoName', this.search);
        });
    },
  },
};
</script>
