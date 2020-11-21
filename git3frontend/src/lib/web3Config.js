module.exports = {
  GIT_FACTORY_ADDRESS: '0x3bFF586A6Cab36Bb87Da89df1d9578691e3328a1',
  RPC_ADDRESS: 'https://rpc-mumbai.matic.today',
  FACTORY_ENS_NAME: 'factory.git3.eth',
  FACTORY_ADDRESS: '0x12aDc3F0dad279597CaE96B744A332004FAE2FeD',
  GIT_FACTORY_INTERFACE: [
    {
      anonymous: false,
      inputs: [
        {
          indexed: false,
          internalType: 'string',
          // eslint-disable-next-line no-restricted-globals
          name,
          type: 'string',
        },
        {
          indexed: false,
          internalType: 'address',
          name: 'user',
          type: 'address',
        },
      ],
      name: 'NewRepositoryCreated',
      type: 'event',
    },
    {
      anonymous: false,
      inputs: [
        {
          indexed: true,
          internalType: 'address',
          name: 'previousOwner',
          type: 'address',
        },
        {
          indexed: true,
          internalType: 'address',
          name: 'newOwner',
          type: 'address',
        },
      ],
      name: 'OwnershipTransferred',
      type: 'event',
    },
    {
      inputs: [
        {
          internalType: 'string',
          name: '',
          type: 'string',
        },
      ],
      name: 'activeRepository',
      outputs: [
        {
          internalType: 'bool',
          name: 'isActive',
          type: 'bool',
        },
        {
          internalType: 'uint256',
          name: 'index',
          type: 'uint256',
        },
      ],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [
        {
          internalType: 'string',
          name: '_repoName',
          type: 'string',
        },
      ],
      name: 'createRepository',
      outputs: [],
      stateMutability: 'nonpayable',
      type: 'function',
    },
    {
      inputs: [
        {
          internalType: 'string',
          name: '_repoName',
          type: 'string',
        },
      ],
      name: 'getRepositoriesUserList',
      outputs: [
        {
          internalType: 'address[]',
          name: '',
          type: 'address[]',
        },
      ],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [],
      name: 'getRepositoryNames',
      outputs: [
        {
          internalType: 'string[]',
          name: '',
          type: 'string[]',
        },
      ],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [
        {
          internalType: 'address',
          name: '_owner',
          type: 'address',
        },
        {
          internalType: 'string',
          name: '_repoName',
          type: 'string',
        },
      ],
      name: 'getUserRepoNameHash',
      outputs: [
        {
          internalType: 'bytes32',
          name: '',
          type: 'bytes32',
        },
      ],
      stateMutability: 'pure',
      type: 'function',
    },
    {
      inputs: [
        {
          internalType: 'address',
          name: '_owner',
          type: 'address',
        },
      ],
      name: 'getUsersRepositories',
      outputs: [
        {
          internalType: 'string[]',
          name: '',
          type: 'string[]',
        },
      ],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [],
      name: 'owner',
      outputs: [
        {
          internalType: 'address',
          name: '',
          type: 'address',
        },
      ],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [
        {
          internalType: 'address',
          name: '_owner',
          type: 'address',
        },
        {
          internalType: 'string',
          name: '_repoName',
          type: 'string',
        },
        {
          internalType: 'uint256',
          name: '_userIndex',
          type: 'uint256',
        },
        {
          internalType: 'uint256',
          name: '_repoIndex',
          type: 'uint256',
        },
      ],
      name: 'removeRepository',
      outputs: [],
      stateMutability: 'nonpayable',
      type: 'function',
    },
    {
      inputs: [],
      name: 'renounceOwnership',
      outputs: [],
      stateMutability: 'nonpayable',
      type: 'function',
    },
    {
      inputs: [
        {
          internalType: 'string',
          name: '',
          type: 'string',
        },
        {
          internalType: 'uint256',
          name: '',
          type: 'uint256',
        },
      ],
      name: 'reposUserList',
      outputs: [
        {
          internalType: 'address',
          name: '',
          type: 'address',
        },
      ],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [
        {
          internalType: 'bytes32',
          name: '',
          type: 'bytes32',
        },
      ],
      name: 'repositoryList',
      outputs: [
        {
          internalType: 'bool',
          name: 'isActive',
          type: 'bool',
        },
        {
          internalType: 'string',
          // eslint-disable-next-line no-restricted-globals
          name,
          type: 'string',
        },
        {
          internalType: 'contract GitRepository',
          name: 'location',
          type: 'address',
        },
      ],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [
        {
          internalType: 'uint256',
          name: '',
          type: 'uint256',
        },
      ],
      name: 'repositoryNames',
      outputs: [
        {
          internalType: 'string',
          name: '',
          type: 'string',
        },
      ],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [
        {
          internalType: 'address',
          name: 'newOwner',
          type: 'address',
        },
      ],
      name: 'transferOwnership',
      outputs: [],
      stateMutability: 'nonpayable',
      type: 'function',
    },
    {
      inputs: [
        {
          internalType: 'address',
          name: '',
          type: 'address',
        },
        {
          internalType: 'uint256',
          name: '',
          type: 'uint256',
        },
      ],
      name: 'usersRepoList',
      outputs: [
        {
          internalType: 'string',
          name: '',
          type: 'string',
        },
      ],
      stateMutability: 'view',
      type: 'function',
    },
  ],
  REPOSITORY_INTERFACE: [
    {
      inputs: [
        {
          internalType: 'address',
          name: '_factory',
          type: 'address',
        },
        {
          internalType: 'string',
          name: '_name',
          type: 'string',
        },
        {
          internalType: 'address',
          name: '_owner',
          type: 'address',
        },
        {
          internalType: 'uint256',
          name: '_userIndex',
          type: 'uint256',
        },
        {
          internalType: 'uint256',
          name: '_repoIndex',
          type: 'uint256',
        },
      ],
      stateMutability: 'nonpayable',
      type: 'constructor',
    },
    {
      anonymous: false,
      inputs: [
        {
          indexed: false,
          internalType: 'string',
          name: 'Cid',
          type: 'string',
        },
      ],
      name: 'NewIssue',
      type: 'event',
    },
    {
      anonymous: false,
      inputs: [
        {
          indexed: false,
          internalType: 'string',
          name: 'branch',
          type: 'string',
        },
        {
          indexed: false,
          internalType: 'string',
          name: 'Cid',
          type: 'string',
        },
      ],
      name: 'NewPush',
      type: 'event',
    },
    {
      anonymous: false,
      inputs: [
        {
          indexed: true,
          internalType: 'address',
          name: 'previousOwner',
          type: 'address',
        },
        {
          indexed: true,
          internalType: 'address',
          name: 'newOwner',
          type: 'address',
        },
      ],
      name: 'OwnershipTransferred',
      type: 'event',
    },
    {
      anonymous: false,
      inputs: [
        {
          indexed: false,
          internalType: 'uint256',
          name: 'amount',
          type: 'uint256',
        },
        {
          indexed: false,
          internalType: 'address',
          name: 'tipper',
          type: 'address',
        },
      ],
      name: 'ReceivedTip',
      type: 'event',
    },
    {
      inputs: [
        {
          internalType: 'uint256',
          name: '',
          type: 'uint256',
        },
      ],
      name: 'branchNames',
      outputs: [
        {
          internalType: 'string',
          name: '',
          type: 'string',
        },
      ],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [
        {
          internalType: 'string',
          name: '',
          type: 'string',
        },
      ],
      name: 'branches',
      outputs: [
        {
          internalType: 'bool',
          name: 'isActive',
          type: 'bool',
        },
        {
          internalType: 'string',
          name: 'headCid',
          type: 'string',
        },
      ],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [],
      name: 'collectTips',
      outputs: [],
      stateMutability: 'nonpayable',
      type: 'function',
    },
    {
      inputs: [],
      name: 'deleteRepository',
      outputs: [],
      stateMutability: 'nonpayable',
      type: 'function',
    },
    {
      inputs: [],
      name: 'getBranchNames',
      outputs: [
        {
          internalType: 'string[]',
          name: '',
          type: 'string[]',
        },
      ],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [
        {
          internalType: 'uint256',
          name: '',
          type: 'uint256',
        },
      ],
      name: 'issues',
      outputs: [
        {
          internalType: 'string',
          name: 'cid',
          type: 'string',
        },
        {
          internalType: 'uint256',
          name: 'bounty',
          type: 'uint256',
        },
      ],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [],
      name: 'owner',
      outputs: [
        {
          internalType: 'address',
          name: '',
          type: 'address',
        },
      ],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [
        {
          internalType: 'string',
          name: 'branch',
          type: 'string',
        },
        {
          internalType: 'string',
          name: 'newCid',
          type: 'string',
        },
      ],
      name: 'push',
      outputs: [],
      stateMutability: 'nonpayable',
      type: 'function',
    },
    {
      inputs: [],
      name: 'renounceOwnership',
      outputs: [],
      stateMutability: 'nonpayable',
      type: 'function',
    },
    {
      inputs: [],
      name: 'repoName',
      outputs: [
        {
          internalType: 'string',
          name: '',
          type: 'string',
        },
      ],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [],
      name: 'tips',
      outputs: [
        {
          internalType: 'uint256',
          name: '',
          type: 'uint256',
        },
      ],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [
        {
          internalType: 'address',
          name: 'newOwner',
          type: 'address',
        },
      ],
      name: 'transferOwnership',
      outputs: [],
      stateMutability: 'nonpayable',
      type: 'function',
    },
    {
      inputs: [
        {
          internalType: 'uint256',
          name: '_newRepoIndex',
          type: 'uint256',
        },
      ],
      name: 'updateRepoIndex',
      outputs: [],
      stateMutability: 'nonpayable',
      type: 'function',
    },
    {
      inputs: [
        {
          internalType: 'uint256',
          name: '_newUserIndex',
          type: 'uint256',
        },
      ],
      name: 'updateUserIndex',
      outputs: [],
      stateMutability: 'nonpayable',
      type: 'function',
    },
    {
      stateMutability: 'payable',
      type: 'receive',
    },
  ],
  IPFS_MULTIADDR: '/ip4/127.0.0.1/tcp/5001',
  // IPFS_ADDRESS: 'http://127.0.0.1:5001',
  IPFS_ADDRESS: 'https://ipfs.infura.io:5001',
  MATIC_RPC: 'https://rpc-mumbai.matic.today',
  GOERLI_RPC: 'https://eth-goerli.gateway.pokt.network/v1/5f8b320bb90218002e9cea2b',
  COINGECKO_URL: 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum',
};
