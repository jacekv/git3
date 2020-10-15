<template>
  <v-app-bar>
    <v-toolbar-title>{{ newRepoName }}</v-toolbar-title>

    <v-dialog
      v-model="dialog"
      width="300"
      v-if="newRepoName != 'Repository Name' && metamaskConnected"
    >
      <template v-slot:activator="{ on: dialog }">
        <v-tooltip right>
          <template v-slot:activator="{ on: tooltip }">
          <v-btn class='ml-4' v-on="{ ...tooltip, ...dialog }"
            fab small outlined @click='getBalance'
          >
            <v-icon>mdi-coffee</v-icon>
          </v-btn>
          </template>
          <span>Tip the repository :)</span>
        </v-tooltip>
      </template>

      <v-card>
        <v-card-title class="headline">
          Tip the repository
        </v-card-title>

        <v-card-text>
          How much would you like to tip?
        </v-card-text>

        <v-card-text>
          You have: {{ eth }} Eth
        </v-card-text>

        <v-card-text>
          <v-text-field type=number v-model=tip>
          </v-text-field>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="tipping"
          >
            Tip
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app-bar>
</template>

<script>
import store from '../store/index';

const Contract = require('web3-eth-contract');
const web3Config = require('../lib/web3Config.js');

const gitFactory = new Contract(web3Config.GIT_FACTORY_INTERFACE, web3Config.GIT_FACTORY_ADDRESS);

function Sleep(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

async function textTx() {
  console.log('The hell');
  await Sleep(5000);
  console.log('The hell');
}

export default {
  name: 'RepositoryHeader',
  data() {
    return {
      dialog: false,
      eth: 0,
      tip: 0,
    };
  },
  computed: {
    newRepoName: () => store.getters.getRepoName,
    metamaskConnected: () => store.getters.isMetaMaskConnected,
  },
  methods: {
    async getBalance() {
      const wei = await this.$web3.eth.getBalance(window.ethereum.selectedAddress);
      this.eth = wei / 1000000000000000000;
      fetch('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum')
        .then((response) => response.json())
        .then((data) => {
          this.tip = 3 / data[0].current_price;
        });
    },
    tipping() {
      console.log('Time to tip the repo');
      console.log((this.tip * 1000000000000000000).toString());
      gitFactory.methods.gitRepositories(store.getters.getRepoName).call()
        .then((address) => {
          console.log('Repository address', address);
          return window.ethereum.request({
            method: 'eth_sendTransaction',
            params: [
              {
                from: window.ethereum.selectedAddress,
                to: address,
                value: (this.tip * 1000000000000000000).toString(16),
                gasPrice: (80).toString(16),
                gas: '21055',
              },
            ],
          });
        })
        .then((txHash) => {
          console.log('txHash', txHash);
          textTx();
          console.log('Need to close the dialog and show pending tx. Like loading coffe mug');
          console.log('While sending the tx, we need to distinguish between Goerli and Matic!');
        })
        .catch(() => console.error);
    },
  },
};
</script>
