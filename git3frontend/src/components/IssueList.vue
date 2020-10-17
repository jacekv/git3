<template>
  <v-simple-table>
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left" style='width: 80px'>Bounty (Wei)</th>
          <th class="text-left">Title</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in files" :key="item.title">
          <td style='width: 80px'>
            {{ item.bounty }} Wei
          </td>
          <td>{{ item.title }}</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
</template>

<script>
import store from '../store/index';

export default {
  name: 'IssueList',

  data() {
    return {
      files: store.getters.getFileList,
    };
  },
};
</script>
