<template>
  <v-app>
    <NavigationBar/>

    <v-main>
      <v-container fluid class='pa-0'>
        <v-row>
          <v-col cols='12' class='py-0'>
            <RepositoryHeader/>
          </v-col>
        </v-row>
        <v-row>
          <v-col v-if='fileExplorer || issues' cols='8' offset='2'>
            <FileExplorer v-if='fileExplorer' />
            <!-- <IssueExplorer v-else-if='issues' /> -->
          </v-col>
          <v-col v-if='logo' cols='8' offset='5'>
            <img src="@/assets/myLogo.png"/>
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <v-footer>
      <template v-if='!pendingTx
        && getRepoOwnerAddress == metamaskAddress
        && metamaskAddress !== ""'
      >
        <v-btn depressed outlined @click="collectTips">
          Collect
        </v-btn>
      </template>
      <v-progress-circular
        indeterminate
        color="amber"
        class="ml-4"
        v-else-if="pendingTx"
      ></v-progress-circular>
      <template v-if='repositoryLoaded'>
        Tips: {{ tips }} Matic
      </template>
      <v-spacer/>
      Powered by Matic
    </v-footer>
  </v-app>
</template>

<script>
import NavigationBar from './components/NavigationBar.vue';
import FileExplorer from './components/FileExplorer.vue';
// import IssueExplorer from './components/IssueExplorer.vue';
import RepositoryHeader from './components/RepositoryHeader.vue';
import store from './store/index';

const web3Config = require('./lib/web3Config.js');

function Sleep(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

export default {
  name: 'App',

  components: {
    NavigationBar,
    FileExplorer,
    RepositoryHeader,
    // IssueExplorer,
  },
  data() {
    return {
      pendingTx: false,
    };
  },
  computed: {
    logo: () => store.getters.showLogo,
    fileExplorer: () => store.getters.showCode,
    issues: () => store.getters.showIssues,
    repositoryLoaded: () => store.getters.getRepositoryLoaded,
    tips: () => store.getters.getTips,
    metamaskAddress: () => store.getters.getMetaMaskAddress.toLowerCase(),
    getRepoOwnerAddress: () => store.getters.getRepoOwnerAddress.toLowerCase(),
  },
  methods: {
    collectTips() {
      console.log('Collecting tips');
      const repoContract = new this.$web3Matic.eth.Contract(
        web3Config.REPOSITORY_INTERFACE, store.getters.getRepoAddress,
      );
      const transactionParameters = {
        gasPrice: '0xB2D05E00', // 3 Gwei
        gas: '0x9C40', // 40000
        to: store.getters.getRepoAddress,
        from: store.getters.getRepoOwnerAddress,
        data: repoContract.methods.collectTips().encodeABI(),
      };
      window.ethereum.request({
        method: 'eth_sendTransaction',
        params: [transactionParameters],
      })
        .then((txHash) => {
          console.log('Tx hash', txHash);
          this.pendingTx = true;
          this.checkTxConfirmed(txHash);
        });
    },
    async checkTxConfirmed(txHash) {
      console.log('Checking tx status');
      let receipt = await this.$web3Matic.eth.getTransactionReceipt(txHash);
      console.log(receipt);
      while (receipt === null) {
        await Sleep(5000); // eslint-disable-line no-await-in-loop
        // eslint-disable-next-line no-await-in-loop
        receipt = await this.$web3Matic.eth.getTransactionReceipt(txHash);
        if (receipt !== null) {
          if (receipt.status) {
            console.log('Transaction has been successful');
            // update tip
            const repoAddress = store.getters.getRepoAddress;
            const repoContract = new this.$web3Matic.eth.Contract(
              web3Config.REPOSITORY_INTERFACE, repoAddress,
            );
            // eslint-disable-next-line no-await-in-loop
            const tips = await repoContract.methods.tips().call();
            store.commit('updateTips', tips / 10 ** 18);
          } else {
            console.log('Transaction has been reverted...');
          }
        } else {
          console.log('Transaction not yet confirmed. Need to check again');
        }
      }
      this.pendingTx = false; // eslint-disable-line no-param-reassign
    },
  },
};
</script>
