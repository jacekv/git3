import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    fileList: [],
    repoName: 'Repository Name',
    repoAddress: '',
    repoOwnerAddress: '',
    repositoryLoaded: false,
    metamaskConnected: false,
    metamaskAddress: '',
    showLogo: true,
    showCode: false,
    showIssues: false,
    tips: 0,
  },
  getters: {
    getFileList: (state) => state.fileList,
    getRepoName: (state) => state.repoName,
    getRepoAddress: (state) => state.repoAddress,
    getRepoOwnerAddress: (state) => state.repoOwnerAddress,
    isMetaMaskConnected: (state) => state.metamaskConnected,
    getMetaMaskAddress: (state) => state.metamaskAddress,
    showLogo: (state) => state.showLogo,
    showCode: (state) => state.showCode,
    showIssues: (state) => state.showIssues,
    getRepositoryLoaded: (state) => state.repositoryLoaded,
    getTips: (state) => state.tips,
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
    updateTips(state, tips) {
      state.tips = tips;
    },
    updateRepoOwnerAddress(state, address) {
      state.repoOwnerAddress = address;
    },
    updateRepoName(state, name) {
      state.repoName = name;
    },
    updateMetaMaskAddress(state, address) {
      state.metamaskAddress = address;
    },
    updateRepositoryLoaded(state, value) {
      state.repositoryLoaded = value;
    },
    updateRepoAddress(state, address) {
      state.repoAddress = address;
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
