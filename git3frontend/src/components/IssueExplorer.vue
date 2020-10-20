<template>
  <v-container>

    <v-row>
      <v-col>
        <v-btn color='amber' v-if='showList' @click='openNewIssue'>
          new issue
        </v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <IssueList v-if='showList'/>
        <IssueInput v-else @clicked='inputAction'/>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import IssueList from './IssueList.vue';
import IssueInput from './IssueInput.vue';
import store from '../store/index';

const Contract = require('web3-eth-contract');
const web3Config = require('../lib/web3Config.js');

const gitFactory = new Contract(web3Config.GIT_FACTORY_INTERFACE, web3Config.GIT_FACTORY_ADDRESS);

export default {
  name: 'IssueExplorer',
  components: {
    IssueList,
    IssueInput,
  },
  data() {
    return {
      showList: true,
    };
  },
  methods: {
    openNewIssue() {
      this.showList = false;
    },
    async inputAction(value) {
      console.log('Emmitted', value);
      if (value === 'cancle') {
        this.showList = true;
      } else if (value === 'openedIssue') {
        this.showList = true;
        const address = await gitFactory.methods
          .gitRepositories(store.getters.getRepoName).call();
        console.log('Address', address);
        const repoContract = new this.$web3.eth.Contract(
          web3Config.REPOSITORY_INTERFACE, address,
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
            issue = await fetch(`${web3Config.IPFS_ADDRESS}/api/v0/dag/get?arg=${issue.cid}`, {
              method: 'POST',
            });
            // eslint-disable-next-line no-await-in-loop
            data = await issue.json();
            console.log('Data', data);
            issues.push(data);
          } catch (e) {
            console.log('EE', e);
            ok = false;
          }
          i += 1;
        }
        store.commit('updateFileList', issues);
      }
    },
    resolveGitFactoryAddress() {
      console.log('Resolved address:', this);
    },
  },
};
</script>
