<template>
  <v-app-bar app>
    <img style="widht: 50px; height: 50px" src="@/assets/myLogo.png" />
    <v-autocomplete
      class="pl-6 shrink"
      style="height: 30px;"
      prepend-icon="mdi-magnify"
      v-model="model"
      :items="items"
      :search-input.sync="searchRepositories"
      clearable
      item-text="name"
      item-value="symbol"
      label="Search repository"
    ></v-autocomplete>
    <v-spacer />
    <v-btn rounded @click="connectMetaMask">
      {{ buttonText }}
    </v-btn>
  </v-app-bar>
</template>

<script>
import store from '../store/index';

const web3Config = require('../lib/web3Config.js');

async function getDataFromIPFS(cid) {
  const response = await fetch(
    `${web3Config.IPFS_ADDRESS}/api/v0/cat?arg=${cid}`,
    {
      method: 'POST',
    },
  );
  return response.json();
}

export default {
  name: 'NavigationBar',
  data() {
    return {
      buttonText: 'Connect to MetaMask',
      items: [],
      value: null,
      model: null,
      searchRepositories: null,
    };
  },
  watch: {
    model(val) {
      // the user decided to pick an entry
      if (val != null) {
        const [partialUserAddress, repoName] = val.split('/');
        const splittedPartialUserAddress = partialUserAddress.split('..');
        // since we only have a partial entry of the address, we need to get all of them again
        // and build it together
        this.$factoryContract.methods.getRepositoriesUserList(repoName).call()
          .then((userAddresses) => {
            // eslint-disable-next-line max-len
            const [userAddress] = userAddresses.filter((entry) => entry.startsWith(splittedPartialUserAddress[0])
              && entry.endsWith(splittedPartialUserAddress[1].trim()));
            return this.$factoryContract.methods.getUserRepoNameHash(userAddress, repoName).call();
          })
          .then((userRepoHash) => this.$factoryContract.methods.repositoryList(userRepoHash).call())
          .then((repo) => {
            const repoContract = new this.$web3Matic.eth.Contract(
              web3Config.REPOSITORY_INTERFACE, repo.location,
            );
            store.commit('updateRepoAddress', repo.location);
            return Promise.all([
              repoContract.methods.branches('main').call(),
              repoContract.methods.tips().call(),
              repoContract.methods.owner().call(),
            ]);
          })
          .then(async ([branch, tips, owner]) => {
            const { headCid } = branch;
            const commit = await getDataFromIPFS(headCid);
            const tree = await getDataFromIPFS(commit.tree);
            const files = [];
            tree.entries.forEach((entry) => {
              files.push({
                name: entry.name,
                type: (entry.mode === 16384 ? 'Directory' : 'File'),
                cid: entry.cid,
              });
            });
            store.commit('updateRepoOwnerAddress', owner);
            store.commit('updateFileList', files);
            store.commit('updateRepoName', val);
            store.commit('updateTips', tips / 10 ** 18);
            store.commit('updateRepositoryLoaded', true);
            store.commit('toggleCode');
            store.commit('toggleLogo');
          });
      }
    },
    searchRepositories(userInput) {
      if (userInput < 3 || userInput === undefined || userInput === null) return;
      // get all repositry names there are
      this.$factoryContract.methods.getRepositoryNames().call()
        .then((repoNames) => {
          // and filter based on the search entered by the user
          const filteredRepoNames = repoNames.filter((entry) => entry.toLowerCase()
            .startsWith(userInput.toLowerCase()));
          // TODO: overtime, we should go over all possible repositories and not only the first one
          // get all user addresses who have a repository by the first name
          return Promise.all([
            this.$factoryContract.methods.getRepositoriesUserList(filteredRepoNames[0]).call(),
            filteredRepoNames[0],
          ]);
        })
        .then(([userList, filteredRepoName]) => {
          // put the user address and the repository name together
          this.items = userList.map((userAddress) => `${userAddress.substring(0, 6)}..
${userAddress.substring(37)}/${filteredRepoName}`);
        })
        .catch(() => {
          console.log('No findings');
        });
    },
  },
  methods: {
    async connectMetaMask() {
      let accounts = [];
      try {
        accounts = await window.ethereum.request({
          method: 'eth_requestAccounts',
        });
      } catch (e) {
        console.log('User rejects MetaMask connection');
      }
      if (accounts.length === 0) return;
      console.log('Address is', accounts);
      store.commit('updateMetaMaskConnectionStatus', true);
      store.commit('updateMetaMaskAddress', accounts[0]);
      [this.buttonText] = accounts;
      this.buttonText = `${this.buttonText.substring(0, 6)}..${this.buttonText.substring(37)}`;
    },
  },
};
</script>
