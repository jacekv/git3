<template>
  <v-simple-table>
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left">Type</th>
          <th class="text-left">Name</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in files" :key="item.name">
          <!-- <td>{{ item.type }}</td> -->
          <td style='width: 20px'>
            <v-icon v-if="item.type == 'Directory'">mdi-folder</v-icon>
            <v-icon v-else>mdi-file</v-icon>
          </td>
          <td>{{ item.name }}</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
</template>

<script>
import store from '../store/index';

export default {
  name: 'FileExplorer',

  data() {
    return {
      files: store.getters.getFileList,
    };
  },
};
</script>
