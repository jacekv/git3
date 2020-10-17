<template>
  <v-form>
    <v-text-field label="Title" outlined v-model="title"> </v-text-field>

    <v-textarea label="Issue" outlined v-model="issueText"> </v-textarea>

    <v-row>
      <v-col cols="2">
        <p class="mb-0 mt-4">Add bounty:</p>
      </v-col>
      <v-col cols="4">
        <v-text-field class="mt-0" type="number" v-model="bounty">
        </v-text-field>
      </v-col>
    </v-row>
    <v-btn color="amber" class="mr-2" @click="submitIssue">
      Submit Issue
    </v-btn>
    <v-btn color="amber" @click="cancleIssueCreation"> Cancle </v-btn>
  </v-form>
</template>

<script>
import store from '../store/index';

const Contract = require('web3-eth-contract');
const web3Config = require('../lib/web3Config.js');

const gitFactory = new Contract(web3Config.GIT_FACTORY_INTERFACE, web3Config.GIT_FACTORY_ADDRESS);

function Sleep(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

export default {
  name: 'IssueInput',

  data() {
    return {
      bounty: 0,
      title: '',
      issueText: '',
    };
  },
  methods: {
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
          this.$emit('clicked', 'openedIssue');
        } else {
          console.log('Transaction not yet confirmed. Need to check again');
        }
      }
      this.pendingTx = false; // eslint-disable-line no-param-reassign
    },
    cancleIssueCreation() {
      this.$emit('clicked', 'cancle');
    },
    submitIssue() {
      const issue = {
        title: this.title,
        issueText: this.issueText,
        bounty: this.bounty,
      };
      const formData = new FormData();
      const blob = new Blob([JSON.stringify(issue)], {
        type: 'application/json',
      });
      formData.append('file', blob);

      fetch(`${web3Config.IPFS_ADDRESS}/api/v0/dag/put`, {
        method: 'POST',
        body: formData,
      })
        .then((r) => r.json())
        .then(async (data) => {
          const address = await gitFactory.methods
            .gitRepositories(store.getters.getRepoName).call();

          const repoContract = new this.$web3.eth.Contract(
            web3Config.REPOSITORY_INTERFACE, address,
          );

          const callData = repoContract.methods
            .openIssue(data.Cid['/'])
            .encodeABI();

          return window.ethereum.request({
            method: 'eth_sendTransaction',
            params: [
              {
                from: window.ethereum.selectedAddress,
                to: address,
                value: this.bounty.toString(16),
                gasPrice: '0x77359400', // 2 Gwei
                gas: '0x32F55',
                data: callData,
              },
            ],
          })
            .then((txHash) => {
              this.checkTxConfirmed(txHash);
              console.log('txHash', txHash);
            });
        });
    },
  },
};
</script>
