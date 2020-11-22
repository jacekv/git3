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

export default {
  name: 'App',

  components: {
    NavigationBar,
    FileExplorer,
    RepositoryHeader,
    // IssueExplorer,
  },
  data() {
    return {};
  },
  computed: {
    logo: () => store.getters.showLogo,
    fileExplorer: () => store.getters.showCode,
    issues: () => store.getters.showIssues,
    repositoryLoaded: () => store.getters.getRepositoryLoaded,
    tips: () => store.getters.getTips,
  },
};
</script>
