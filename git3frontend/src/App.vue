<template>
  <v-app>
    <NavigationBar/>

    <v-content>
      <v-container fluid class='pa-0'>
        <v-row>
          <v-col cols='12' class='py-0'>
            <RepositoryHeader/>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols='8' offset='2'>
            <FileExplorer/>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import NavigationBar from './components/NavigationBar.vue';
import FileExplorer from './components/FileExplorer.vue';
import RepositoryHeader from './components/RepositoryHeader.vue';
import store from './store/index';

console.log(store.getters);
export default {
  name: 'App',

  components: {
    NavigationBar,
    FileExplorer,
    RepositoryHeader,
  },
  data() {
    return {};
  },
};
</script>
