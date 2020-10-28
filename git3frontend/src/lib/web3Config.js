module.exports = {
  GIT_FACTORY_ADDRESS: '0x3bFF586A6Cab36Bb87Da89df1d9578691e3328a1',
  RPC_ADDRESS: 'https://rpc-mumbai.matic.today',
  FACTORY_ENS_NAME: 'factory.git3.eth',
  GIT_FACTORY_INTERFACE: [
    {
      inputs: [],
      stateMutability: 'nonpayable',
      type: 'constructor',
    },
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
          internalType: 'contract GitRepository',
          name: 'Address',
          type: 'address',
        },
      ],
      name: 'CreatedNewRepository',
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
          // eslint-disable-next-line no-restricted-globals
          name,
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
          name: '',
          type: 'string',
        },
      ],
      name: 'gitRepositories',
      outputs: [
        {
          internalType: 'contract GitRepository',
          name: '',
          type: 'address',
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
      inputs: [],
      name: 'renounceOwnership',
      outputs: [],
      stateMutability: 'nonpayable',
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
  ],
  REPOSITORY_INTERFACE: [
    {
      inputs: [
        {
          internalType: 'string',
          // eslint-disable-next-line no-restricted-globals
          name,
          type: 'string',
        },
        {
          internalType: 'address',
          name: 'owner',
          type: 'address',
        },
      ],
      stateMutability: 'nonpayable',
      type: 'constructor',
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
          name: '',
          type: 'uint256',
        },
      ],
      name: 'cidHistory',
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
      name: 'getCidHistory',
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
      name: 'headCid',
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
      inputs: [
        {
          internalType: 'string',
          name: '',
          type: 'string',
        },
      ],
      name: 'pushHistory',
      outputs: [
        {
          internalType: 'bool',
          name: '',
          type: 'bool',
        },
      ],
      stateMutability: 'view',
      type: 'function',
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
          name: 'Cid',
          type: 'string',
        },
      ],
      name: 'NewPush',
      type: 'event',
    },
    {
      inputs: [
        {
          internalType: 'string',
          name: 'cid',
          type: 'string',
        },
      ],
      name: 'openIssue',
      outputs: [],
      stateMutability: 'payable',
      type: 'function',
    },
    {
      stateMutability: 'payable',
      type: 'receive',
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
  ],
  IPFS_MULTIADDR: '/ip4/127.0.0.1/tcp/5001',
  // IPFS_ADDRESS: 'http://127.0.0.1:5001',
  IPFS_ADDRESS: 'https://ipfs.infura.io:5001',
  MATIC_RPC: 'https://rpc-mumbai.matic.today',
  GOERLI_RPC: 'https://eth-goerli.gateway.pokt.network/v1/5f8b320bb90218002e9cea2b',
  COINGECKO_URL: 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum',
};
