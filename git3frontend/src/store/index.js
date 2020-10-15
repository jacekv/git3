import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    fileList: [],
    repoName: 'Repository Name',
    metamaskConnected: false,
  },
  getters: {
    getFileList: (state) => state.fileList,
    getRepoName: (state) => state.repoName,
    isMetaMaskConnected: (state) => state.metamaskConnected,
  },
  mutations: {
    updateFileList(state, files) {
      for (let i = 0; i < files.length; i += 1) {
        Vue.set(state.fileList, i, files[i]);
      }
    },
    updateRepoName(state, name) {
      state.repoName = name;
    },
    updateMetaMaskConnectionStatus(state, status) {
      state.metamaskConnected = status;
    },
  },
  actions: {
  },
  modules: {
  },
});
