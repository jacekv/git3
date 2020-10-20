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

const web3Config = require('../lib/web3Config.js');

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
      if (value === 'cancle') {
        this.showList = true;
      } else if (value === 'openedIssue') {
        this.showList = true;
        const address = await this.$factoryContract.methods
          .gitRepositories(store.getters.getRepoName).call();
        const repoContract = new this.$web3Matic.eth.Contract(
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
            // console.log('Data', data);
            issues.push(data);
          } catch (e) {
            // console.log('EE', e);
            ok = false;
          }
          i += 1;
        }
        store.commit('updateFileList', issues);
      }
    },
  },
};
</script>
