<template>
  <v-app-bar>
    <v-toolbar-title>{{ newRepoName }}</v-toolbar-title>

    <v-dialog
      v-model="dialog"
      width="300"
      v-if="newRepoName != 'Repository Name' && metamaskConnected && !pendingTx"
    >
      <template v-slot:activator="{ on: dialog }">
        <v-tooltip right>
          <template v-slot:activator="{ on: tooltip }">
            <v-btn
              class="ml-4"
              v-on="{ ...tooltip, ...dialog }"
              fab
              small
              outlined
              @click="getBalance"
            >
              <v-icon>mdi-coffee</v-icon>
            </v-btn>
          </template>
          <span>Tip the repository :)</span>
        </v-tooltip>
      </template>

      <v-card>
        <v-card-title class="headline"> Tip the repository </v-card-title>

        <v-card-text> How much would you like to tip? </v-card-text>

        <v-card-text> You have: {{ eth }} Eth </v-card-text>

        <v-card-text>
          <v-text-field type="number" v-model="tip"> </v-text-field>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="tipping"> Tip </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-progress-circular
      indeterminate
      color="amber"
      class="ml-4"
      v-else-if="pendingTx"
    ></v-progress-circular>
    <v-spacer></v-spacer>
    <v-btn depressed :outlined="showCode" @click="enableCode"> /code </v-btn>
    <v-btn depressed :outlined="showIssues" @click="enableIssues">
      /issues
    </v-btn>
  </v-app-bar>
</template>

<script>
import store from '../store/index';

const Contract = require('web3-eth-contract');
const web3Config = require('../lib/web3Config.js');

const gitFactory = new Contract(
  web3Config.GIT_FACTORY_INTERFACE,
  web3Config.GIT_FACTORY_ADDRESS,
);

function Sleep(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

export default {
  name: 'RepositoryHeader',
  data() {
    return {
      dialog: false,
      eth: 0,
      tip: 0,
      pendingTx: false,
    };
  },
  computed: {
    newRepoName: () => store.getters.getRepoName,
    metamaskConnected: () => store.getters.isMetaMaskConnected,
    showCode: () => store.getters.showCode,
    showIssues: () => store.getters.showIssues,
  },
  methods: {
    async getBalance() {
      const wei = await this.$web3.eth.getBalance(
        window.ethereum.selectedAddress,
      );
      this.eth = wei / 1000000000000000000;
      fetch(
        'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum',
      )
        .then((response) => response.json())
        .then((data) => {
          this.tip = 3 / data[0].current_price;
        });
    },
    tipping() {
      gitFactory.methods
        .gitRepositories(store.getters.getRepoName)
        .call()
        .then((address) => {
          console.log(address);
          // const { networkVersion } = window.ethereum;
          // if (networkVersion === '80001') {
          //   console.log('We are on Matic :)');
          //   return window.ethereum.request({
          //     method: 'eth_sendTransaction',
          //     params: [
          //       {
          //         from: window.ethereum.selectedAddress,
          //         to: address,
          //         value: (this.tip * 1000000000000000000).toString(16),
          //         gasPrice: '0x12A05F2000',
          //         gas: '21055',
          //       },
          //     ],
          //   });
          // } else if (networkVersion === '5') {
          //   console.log('We are on Goerli :)');
          // }
          return window.ethereum.request({
            method: 'eth_sendTransaction',
            params: [
              {
                from: window.ethereum.selectedAddress,
                to: address,
                value: (this.tip * 1000000000000000000).toString(16),
                gasPrice: '0x77359400', // 2 Gwei
                gas: '0x523F', // 21055
              },
            ],
          });
        })
        .then((txHash) => {
          this.dialog = false;
          this.pendingTx = true;
          this.checkTxConfirmed(txHash);
          console.log(
            'While sending the tx, we need to distinguish between Goerli and Matic!',
          );
        })
        .catch(() => console.error);
    },
    async checkTxConfirmed(txHash) {
      console.log('Checking tx status');
      let receipt = await this.$web3.eth.getTransactionReceipt(txHash);
      console.log(receipt);
      while (receipt === null) {
        await Sleep(5000); // eslint-disable-line no-await-in-loop
        // eslint-disable-next-line no-await-in-loop
        receipt = await this.$web3.eth.getTransactionReceipt(txHash);
        if (receipt !== null) {
          if (receipt.status) {
            console.log('Transaction has been successful');
          } else {
            console.log('Transaction has been reverted...');
          }
        } else {
          console.log('Transaction not yet confirmed. Need to check again');
        }
      }
      this.pendingTx = false; // eslint-disable-line no-param-reassign
    },
    enableCode() {
      if (!store.getters.showCode) {
        store.commit('toggleCode');
        store.commit('toggleIssues');
      }
    },
    async enableIssues() {
      if (!store.getters.showIssues) {
        store.commit('toggleIssues');
        store.commit('toggleCode');
      }
      const address = await gitFactory.methods
        .gitRepositories(store.getters.getRepoName)
        .call();
      console.log('Address', address);
      const repoContract = new this.$web3.eth.Contract(
        web3Config.REPOSITORY_INTERFACE,
        address,
      );

      let i = 0;
      let ok = true;
      const issues = [];
      let data = '';
      while (ok) {
        try {
          // eslint-disable-next-line no-await-in-loop
          let issue = await repoContract.methods.issues(i).call();
          console.log(issue);
          // eslint-disable-next-line no-await-in-loop
          issue = await fetch(
            `${web3Config.IPFS_ADDRESS}/api/v0/dag/get?arg=${issue.cid}`,
            {
              method: 'POST',
            },
          );
          // eslint-disable-next-line no-await-in-loop
          data = await issue.json();
          console.log('Data', data);
          issues.push(data);
          // console.log('Issues', issues);
        } catch (e) {
          console.log('EE', e);
          ok = false;
        }
        i += 1;
      }
      store.commit('updateFileList', issues);
    },
  },
};
</script>
