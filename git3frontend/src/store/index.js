import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    fileList: [],
    repoName: 'Repository Name',
    metamaskConnected: false,
    showLogo: true,
    showCode: false,
    showIssues: false,
  },
  getters: {
    getFileList: (state) => state.fileList,
    getRepoName: (state) => state.repoName,
    isMetaMaskConnected: (state) => state.metamaskConnected,
    showLogo: (state) => state.showLogo,
    showCode: (state) => state.showCode,
    showIssues: (state) => state.showIssues,
  },
  mutations: {
    updateFileList(state, files) {
      const length = files.length > state.fileList.length ? files.length : state.fileList.length;
      let delPosition;
      for (let i = 0; i < length; i += 1) {
        if (files[i] === undefined) {
          if (delPosition === undefined) {
            delPosition = i;
          }
          Vue.delete(state.fileList, delPosition);
        } else {
          Vue.set(state.fileList, i, files[i]);
        }
      }
    },
    updateRepoName(state, name) {
      state.repoName = name;
    },
    updateMetaMaskConnectionStatus(state, status) {
      state.metamaskConnected = status;
    },
    toggleCode(state) {
      state.showCode = !state.showCode;
    },
    toggleIssues(state) {
      state.showIssues = !state.showIssues;
    },
    toggleLogo(state) {
      state.showLogo = !state.showLogo;
    },
  },
  actions: {
  },
  modules: {
  },
});
