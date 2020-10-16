<template>
  <v-container>

    <v-row>
      <v-col>
        <v-btn color='amber' @click='openNewIssue'>
          new issue
        </v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <IssueList v-if='showList'/>
        <IssueInput v-else />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import IssueList from './IssueList.vue';
import IssueInput from './IssueInput.vue';

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
  },
};
</script>
