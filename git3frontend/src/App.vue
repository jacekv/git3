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
          <v-col cols='8' offset='2'>
            <FileExplorer v-if='fileExplorer' />
            <IssueExplorer v-else-if='issues' />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import NavigationBar from './components/NavigationBar.vue';
import FileExplorer from './components/FileExplorer.vue';
import IssueExplorer from './components/IssueExplorer.vue';
import RepositoryHeader from './components/RepositoryHeader.vue';
import store from './store/index';

export default {
  name: 'App',

  components: {
    NavigationBar,
    FileExplorer,
    RepositoryHeader,
    IssueExplorer,
  },
  data() {
    return {};
  },
  computed: {
    fileExplorer: () => store.getters.showCode,
    issues: () => store.getters.showIssues,
  },
};
</script>
