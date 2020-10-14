<template>
  <v-app-bar>
    <v-toolbar-title>{{ newRepoName }}</v-toolbar-title>
    <v-tooltip right v-if="newRepoName != 'Repository Name'">
      <template v-slot:activator="{ on, attrs }">
        <v-icon class='ml-4' v-bind="attrs" v-on="on">mdi-coffee</v-icon>
      </template>
      <span>Tip repo for some coffee :)</span>
    </v-tooltip>
  </v-app-bar>
</template>

<script>
import store from '../store/index';

export default {
  name: 'RepositoryHeader',
  data() {
    return {};
  },
  computed: {
    newRepoName: () => store.getters.getRepoName,
  },
};
</script>
