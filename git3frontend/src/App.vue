<template>
  <v-app>
    <v-app-bar app>
      <NavigationBar/>
    </v-app-bar>
    <v-content>
      <v-container>
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

export default {
  name: 'App',

  components: {
    NavigationBar,
    FileExplorer,
  },

  data: () => ({
    //
  }),
};
</script>
