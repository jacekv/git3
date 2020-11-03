"""Implement just enough git to commit and push to GitHub.

Read the story here: http://benhoyt.com/writings/pygit/

Released under a permissive MIT license (see LICENSE.txt).
"""
from web3 import Web3
from getpass import getpass
from pathlib import Path

import argparse, collections, difflib, enum, hashlib, operator, os, stat
import struct, sys, time, urllib.request, zlib
import shutil
import ipfshttpclient
import binascii

# Data for one entry in the git index (.git/index)
IndexEntry = collections.namedtuple('IndexEntry', [
    'ctime_s', 'ctime_n', 'mtime_s', 'mtime_n', 'dev', 'ino', 'mode', 'uid',
    'gid', 'size', 'sha1', 'flags', 'path',
])

# mode of the file 33188 -> o100644 
# 100644 is a normal file in git
GIT_NORMAL_FILE_MODE = 33188
GIT_TREE_MODE = 16384

RPC_ADDRESS = 'https://rpc-mumbai.matic.today'
GIT_FACTORY_ADDRESS = '0x3bFF586A6Cab36Bb87Da89df1d9578691e3328a1'
USER_ADDRESS = '0xeC41371D14F7be781301FdD2B39556e7F353D201'
IPFS_CONNECTION = '/ip4/127.0.0.1/tcp/5001'
FACTORY_ABI = '''
[
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "string",
				"name": "Name",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "contract GitRepository",
				"name": "Address",
				"type": "address"
			}
		],
		"name": "CreatedNewRepository",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "previousOwner",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "OwnershipTransferred",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			}
		],
		"name": "createRepository",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "gitRepositories",
		"outputs": [
			{
				"internalType": "contract GitRepository",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "renounceOwnership",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "transferOwnership",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]
'''


REPOSITORY_ABI = '''
[
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "previousOwner",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "OwnershipTransferred",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "newCid",
				"type": "string"
			}
		],
		"name": "push",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "renounceOwnership",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "transferOwnership",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "cidHistory",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getCidHistory",
		"outputs": [
			{
				"internalType": "string[]",
				"name": "",
				"type": "string[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "headCid",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "repoName",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
'''


class NoRepositoryError(Exception):
    """
    Exception raised for not finding a .git folder.

    Attributes:
        message -- Error message
    """
    def __init__(self, message):
        self.message = message

class ObjectType(enum.Enum):
    """Object type enum. There are other types too, but we don't need them.
    See "enum object_type" in git's source (git/cache.h).
    """
    commit = 1
    tree = 2
    blob = 3


def read_file(path):
    """Read contents of file at given path as bytes."""
    with open(path, 'rb') as f:
        return f.read()


def write_file(path, data):
    """Write data bytes to file at given path."""
    with open(path, 'wb') as f:
        f.write(data)


def init(repo):
    """
    Create .git directory for repository and fill with directories and files.
    """
    if os.path.exists(os.path.join(repo, '.git')):
        print('.git folder exists already')
        return

    cwd = os.getcwd()
    if repo != '.':
        os.mkdir(repo)
        repoName = repo
        fullPath = cwd + '/' + repo
    else:
        repoName = cwd.split('/')[-1]
        fullPath = cwd

    os.mkdir(os.path.join(repo, '.git'))
    # create necessary directories
    for name in ['objects', 'refs', 'refs/heads']:
        os.mkdir(os.path.join(repo, '.git', name))
    write_file(os.path.join(repo, '.git', 'HEAD'), b'ref: refs/heads/master')

    # write the name of the repository into a file
    write_file(os.path.join(repo, '.git', 'name'), str.encode(repoName))
        
    print('Initialized empty Git3 repository in: {}/.git/'.format(fullPath))


def hash_object(data, obj_type, write=True):
    """Compute hash of object data of given type and write to object store if
    "write" is True. Return SHA-1 object hash as hex string.
    """
    try:
        repo_root_path = get_repo_root_path()
    except NoRepositoryError as nre:
        raise NoRepositoryError(nre)
    header = '{} {}'.format(obj_type, len(data)).encode()
    full_data = header + b'\x00' + data
    sha1 = hashlib.sha1(full_data).hexdigest()
    if write:
        path = os.path.join(repo_root_path, '.git', 'objects', sha1[:2], sha1[2:])
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            write_file(path, zlib.compress(full_data))
    return sha1


def find_object(sha1_prefix):
    """Find object with given SHA-1 prefix and return path to object in object
    store, or raise ValueError if there are no objects or multiple objects
    with this prefix.
    """
    if len(sha1_prefix) < 2:
        raise ValueError('hash prefix must be 2 or more characters')
    obj_dir = os.path.join('.git', 'objects', sha1_prefix[:2])
    rest = sha1_prefix[2:]
    objects = [name for name in os.listdir(obj_dir) if name.startswith(rest)]
    if not objects:
        raise ValueError('object {!r} not found'.format(sha1_prefix))
    if len(objects) >= 2:
        raise ValueError('multiple objects ({}) with prefix {!r}'.format(
                len(objects), sha1_prefix))
    return os.path.join(obj_dir, objects[0])


def read_object(sha1_prefix):
    """Read object with given SHA-1 prefix and return tuple of
    (object_type, data_bytes), or raise ValueError if not found.
    """
    path = find_object(sha1_prefix)
    full_data = zlib.decompress(read_file(path))
    nul_index = full_data.index(b'\x00')
    header = full_data[:nul_index]
    obj_type, size_str = header.decode().split()
    size = int(size_str)
    data = full_data[nul_index + 1:]
    assert size == len(data), 'expected size {}, got {} bytes'.format(
            size, len(data))
    return (obj_type, data)


def cat_file(mode, sha1_prefix):
    """Write the contents of (or info about) object with given SHA-1 prefix to
    stdout. If mode is 'commit', 'tree', or 'blob', print raw data bytes of
    object. If mode is 'size', print the size of the object. If mode is
    'type', print the type of the object. If mode is 'pretty', print a
    prettified version of the object.
    """
    obj_type, data = read_object(sha1_prefix)
    if mode in ['commit', 'tree', 'blob']:
        if obj_type != mode:
            raise ValueError('expected object type {}, got {}'.format(
                    mode, obj_type))
        sys.stdout.buffer.write(data)
    elif mode == 'size':
        print(len(data))
    elif mode == 'type':
        print(obj_type)
    elif mode == 'pretty':
        if obj_type in ['commit', 'blob']:
            sys.stdout.buffer.write(data)
        elif obj_type == 'tree':
            for mode, path, sha1 in read_tree(data=data):
                type_str = 'tree' if stat.S_ISDIR(mode) else 'blob'
                print('{:06o} {} {}\t{}'.format(mode, type_str, sha1, path))
        else:
            assert False, 'unhandled object type {!r}'.format(obj_type)
    else:
        raise ValueError('unexpected mode {!r}'.format(mode))

def create():
    git_factory = get_factory_contract()
    repo_name = read_repo_name()
    w3 = get_web3_provider()
    if repo_name == '':
        print('There is no repository name.')
        return
    #TODO: calc address from piv key :)
    nonce = w3.eth.getTransactionCount(USER_ADDRESS)
    #priv_key= bytes.fromhex(getpass('Provide priv key: '))
    priv_key = bytes.fromhex(os.environ['PRIV_KEY'])
    create_repo_tx = git_factory.functions.createRepository(repo_name).buildTransaction({
        'chainId': 80001,
        'gas': 1947750,
        'gasPrice': w3.toWei('2', 'gwei'),
        'nonce': nonce,
    })
    signed_txn = w3.eth.account.sign_transaction(create_repo_tx, private_key=priv_key)
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    if receipt['status']:
        print('Repository {:s} has been created'.format(repo_name))
    else:
        print('Creating {:s} repository failed'.format(repo_name))
        print(receipt)

def get_web3_provider():
    return Web3(Web3.HTTPProvider(RPC_ADDRESS))

def get_remote_cid_history():
    git_factory = get_factory_contract()
    repo_name = read_repo_name()
    git_repo_address = git_factory.functions.gitRepositories(repo_name).call()
    repo_contract = get_repository_contract(git_repo_address)
    return repo_contract.functions.getCidHistory().call()

def push_new_cid(cid):
    git_factory = get_factory_contract()
    repo_name = read_repo_name()
    git_repo_address = git_factory.functions.gitRepositories(repo_name).call()
    repo_contract = get_repository_contract(git_repo_address)

    w3 = get_web3_provider()
    nonce = w3.eth.getTransactionCount(USER_ADDRESS)
    #priv_key= bytes.fromhex(getpass('Provide priv key: '))
    priv_key = bytes.fromhex(os.environ['PRIV_KEY'])
    create_push_tx = repo_contract.functions.push(cid).buildTransaction({
        'chainId': 80001,
        'gas': 746427,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce,
    })
    signed_txn = w3.eth.account.sign_transaction(create_push_tx, private_key=priv_key)
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    if receipt['status']:
        print('Successfully pushed')
    else:
        print('Pushing failed')

def clone(repo_name):
    git_factory = get_factory_contract()
    git_repo_address = git_factory.functions.gitRepositories(repo_name).call()
    if git_repo_address == '0x0000000000000000000000000000000000000000':
        print('No such repository')
        return
    repo_contract = get_repository_contract(git_repo_address)
    headCid = repo_contract.functions.headCid().call()
    print('Cloning {:s}'.format(repo_name))
    client = ipfshttpclient.connect(IPFS_CONNECTION)
    #client = ipfshttpclient.connect('/dns/ipfs.infura.io/tcp/5001/https')
    client.get(headCid)
    os.rename(headCid, repo_name)
    client.close()
    print('{:s} cloned'.format(repo_name))
    
def get_factory_contract():
    w3 = get_web3_provider()
    return w3.eth.contract(address=GIT_FACTORY_ADDRESS, abi=FACTORY_ABI)

def get_repository_contract(address):
    w3 = get_web3_provider()
    return w3.eth.contract(address=address, abi=REPOSITORY_ABI)

def check_if_repo_created():
    """
    Checks if the repository has been already registered in the gitFactory contract
    If it hasn't, False is returned, otherwise True
    """
    repo_name = read_repo_name()
    w3 = get_web3_provider()
    if not w3.isConnected():
        #TODO: Throw an exception
        print('No connection. Establish a connection first')
        return False
    gitFactory = get_factory_contract()
    address = gitFactory.functions.gitRepositories(repo_name).call()
    if address == '0x0000000000000000000000000000000000000000':
        return False
    return True
        
def read_repo_name():
    """Read the repoName file and return the name"""
    try:
        data = read_file(os.path.join('.git', 'name'))
    except FileNotFoundError:
        return ""
    return data.rstrip().decode('ascii')

def read_index():
    """Read git index file and return list of IndexEntry objects."""
    try:
        repo_root_path = get_repo_root_path()
        data = read_file(os.path.join(repo_root_path, '.git', 'index'))
    except FileNotFoundError:
        return []
    except NoRepositoryError as nre:
        raise NoRepositoryError(nre)
    digest = hashlib.sha1(data[:-20]).digest()
    assert digest == data[-20:], 'invalid index checksum'
    signature, version, num_entries = struct.unpack('!4sLL', data[:12])
    assert signature == b'DIRC', \
            'invalid index signature {}'.format(signature)
    assert version == 2, 'unknown index version {}'.format(version)
    entry_data = data[12:-20]
    entries = []
    i = 0
    while i + 62 < len(entry_data):
        fields_end = i + 62
        fields = struct.unpack('!LLLLLLLLLL20sH', entry_data[i:fields_end])
        path_end = entry_data.index(b'\x00', fields_end)
        path = entry_data[fields_end:path_end]
        entry = IndexEntry(*(fields + (path.decode(),)))
        entries.append(entry)
        entry_len = ((62 + len(path) + 8) // 8) * 8
        i += entry_len
    assert len(entries) == num_entries
    return entries


def ls_files(details=False):
    """Print list of files in index (including mode, SHA-1, and stage number
    if "details" is True).
    """
    for entry in read_index():
        if details:
            stage = (entry.flags >> 12) & 3
            print('{:6o} {} {:}\t{}'.format(
                    entry.mode, entry.sha1.hex(), stage, entry.path))
        else:
            print(entry.path)


def get_status():
    """
    Get status of working copy, return tuple of
    (changed_paths, new_paths, deleted_paths).
    """
    paths = set()
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d != '.git']
        for file in files:
            path = os.path.join(root, file)
            path = path.replace('\\', '/')
            if path.startswith('./'):
                path = path[2:]
            paths.add(path)
    entries_by_path = {e.path: e for e in read_index()}
    entry_paths = set(entries_by_path)
    changed = {p for p in (paths & entry_paths)
               if hash_object(read_file(p), 'blob', write=False) !=
                  entries_by_path[p].sha1.hex()}
    new = paths - entry_paths
    deleted = entry_paths - paths
    return (sorted(changed), sorted(new), sorted(deleted))


def status():
    """Show status of working copy."""
    changed, new, deleted = get_status()
    if changed:
        print('changed files:')
        for path in changed:
            print('   ', path)
    if new:
        print('new files:')
        for path in new:
            print('   ', path)
    if deleted:
        print('deleted files:')
        for path in deleted:
            print('   ', path)


def diff():
    """Show diff of files changed (between index and working copy)."""
    changed, _, _ = get_status()
    entries_by_path = {e.path: e for e in read_index()}
    for i, path in enumerate(changed):
        sha1 = entries_by_path[path].sha1.hex()
        obj_type, data = read_object(sha1)
        assert obj_type == 'blob'
        index_lines = data.decode().splitlines()
        working_lines = read_file(path).decode().splitlines()
        diff_lines = difflib.unified_diff(
                index_lines, working_lines,
                '{} (index)'.format(path),
                '{} (working copy)'.format(path),
                lineterm='')
        for line in diff_lines:
            print(line)
        if i < len(changed) - 1:
            print('-' * 70)


def write_index(entries):
    """Write list of IndexEntry objects to git index file."""
    try:
        repo_root_path = get_repo_root_path()
    except NoRepositoryError as nre:
        raise NoRepositoryError(nre)
    packed_entries = []

    for entry in entries:
        entry_head = struct.pack('!LLLLLLLLLL20sH',
                entry.ctime_s, entry.ctime_n, entry.mtime_s, entry.mtime_n,
                entry.dev, entry.ino & 0xFFFFFFFF, entry.mode, entry.uid, entry.gid,
                entry.size, entry.sha1, entry.flags)
        path = entry.path.encode()
        length = ((62 + len(path) + 8) // 8) * 8
        packed_entry = entry_head + path + b'\x00' * (length - 62 - len(path))
        packed_entries.append(packed_entry)
    header = struct.pack('!4sLL', b'DIRC', 2, len(entries))
    all_data = header + b''.join(packed_entries)
    digest = hashlib.sha1(all_data).digest()
    write_file(os.path.join(repo_root_path, '.git', 'index'), all_data + digest)
    


def get_repo_root_path():
    """
    Finds the root path of the repository where the .git folder resides and returns the path.
    If no .git folder is found, returns False
    """
    path_to_test = Path(os.getcwd())
    contains_git_folder = os.path.isdir(str(path_to_test) + '/.git')
    if contains_git_folder:
        return str(path_to_test)
    parent = 0
    while not contains_git_folder and str(path_to_test.parents[parent]) != '/':
        contains_git_folder = os.path.isdir(str(path_to_test.parents[parent]) + '/.git')
        if contains_git_folder:
            break
        parent += 1
    if contains_git_folder:
        return str(path_to_test.parents[parent])
    raise NoRepositoryError('Haven\'t found a git repository. Init one first.')


def add(paths):
    """Add all file paths to git index."""
    try:
        repo_root_path = get_repo_root_path()
    except NoRepositoryError as nre:
        print(nre)
        exit(1)

    paths = [p.replace('\\', '/') for p in paths]
    all_entries = []
    # transfer paths to relative paths. Relative to the repository root
    paths = list(map(lambda path: os.path.relpath(os.path.abspath(path), repo_root_path), paths))

    try:
        all_entries = read_index()
    except NoRepositoryError as nre:
        print(nre)
        exit(1)

    entries = [e for e in all_entries if e.path not in paths]
    for path in paths:
        file_path = repo_root_path + '/' + path
        sha1 = hash_object(read_file(file_path), 'blob')
        st = os.stat(file_path)
        #TODO: We will need to check for the file mode properly!
        mode = GIT_NORMAL_FILE_MODE
        flags = len(file_path.encode())
        assert flags < (1 << 12)
        # gets the relative path to the repository root folder for the index file
        relative_path = os.path.relpath(os.path.abspath(file_path), repo_root_path)
        entry = IndexEntry(
                int(st.st_ctime), 0, int(st.st_mtime), 0, st.st_dev,
                st.st_ino, mode, st.st_uid, st.st_gid, st.st_size,
                bytes.fromhex(sha1), flags, relative_path)
        entries.append(entry)
    entries.sort(key=operator.attrgetter('path'))
    write_index(entries)


def write_tree():
    """Write a tree object from the current index entries."""
    tree_entries = []
    tree_to_process = {'.': []}
    indexEntries = read_index()
    for entry in indexEntries:
        if '/' in entry.path:
            path = '/'.join(entry.path.split('/')[0:-1])
        else:
            path = '.'

        if path in tree_to_process:
            tree_to_process[path].append(entry)
        else:
            tree_to_process[path] = [entry]

        # check if path is a directory and not a path to a sub directory
        # if so, add it to the root dir
        if path != '.' and '/' not in path:
            if '.' in tree_to_process and path not in tree_to_process['.']:
                tree_to_process['.'].append(path)
            elif '.' in tree_to_process and path not in tree_to_process['.']:
                tree_to_process['.'] = [path]
        elif '/' in path:
            # if there is subdirectory in a directory we add it
            key = '/'.join(path.split('/')[0:-1])
            if key in tree_to_process:
                tree_to_process[key].append(path)
            else:
                tree_to_process[key] = [path]

    for entry in tree_to_process['.']:
        if isinstance(entry, IndexEntry):
            mode_path = '{:o} {}'.format(entry.mode, entry.path).encode()
            tree_entry = mode_path + b'\x00' + entry.sha1
            tree_entries.append(tree_entry)
        elif isinstance(entry, str):
            tree_hash = __write_subtree(tree_to_process, entry)
            mode_path = '{:o} {}'.format(GIT_TREE_MODE, entry).encode()
            tree_entry = mode_path + b'\x00' + binascii.unhexlify(tree_hash)
            tree_entries.append(tree_entry)
    return hash_object(b''.join(tree_entries), 'tree')

def __write_subtree(indexEntries, dirName):
    """
    Create a subtree for a subdirectories which is going to be added to the normal tree
    """
    tree_entries = []
    for entry in indexEntries[dirName]:
        if isinstance(entry, IndexEntry):
            mode_path = '{:o} {}'.format(entry.mode, entry.path.split('/')[-1]).encode()
            tree_entry = mode_path + b'\x00' + entry.sha1
            tree_entries.append(tree_entry)
        elif isinstance(entry, str):
            tree_hash = __write_subtree(indexEntries, entry)
            mode_path = '{:o} {}'.format(GIT_TREE_MODE, entry.split('/')[-1]).encode()
            tree_entry = mode_path + b'\x00' + binascii.unhexlify(tree_hash)
            tree_entries.append(tree_entry)
    return hash_object(b''.join(tree_entries), 'tree')

def get_local_master_hash():
    """Get current commit hash (SHA-1 string) of local master branch."""
    master_path = os.path.join('.git', 'refs', 'heads', 'master')
    try:
        return read_file(master_path).decode().strip()
    except FileNotFoundError:
        return None


def commit(message, author=None):
    """Commit the current state of the index to master with given message.
    Return hash of commit object.
    """
    # we are working on write tree
    tree = write_tree()
    parent = get_local_master_hash()
    if author is None:
        author = '{} <{}>'.format(
                os.environ['GIT_AUTHOR_NAME'], os.environ['GIT_AUTHOR_EMAIL'])
    timestamp = int(time.mktime(time.localtime()))
    utc_offset = -time.timezone
    author_time = '{} {}{:02}{:02}'.format(
            timestamp,
            '+' if utc_offset > 0 else '-',
            abs(utc_offset) // 3600,
            (abs(utc_offset) // 60) % 60)
    lines = ['tree ' + tree]
    if parent:
        lines.append('parent ' + parent)
    lines.append('author {} {}'.format(author, author_time))
    lines.append('committer {} {}'.format(author, author_time))
    lines.append('')
    lines.append(message)
    lines.append('')
    data = '\n'.join(lines).encode()
    sha1 = hash_object(data, 'commit')
    master_path = os.path.join('.git', 'refs', 'heads', 'master')
    write_file(master_path, (sha1 + '\n').encode())
    print('committed to master: {:7}'.format(sha1))
    return sha1


def extract_lines(data):
    """Extract list of lines from given server data."""
    lines = []
    i = 0
    for _ in range(1000):
        line_length = int(data[i:i + 4], 16)
        line = data[i + 4:i + line_length]
        lines.append(line)
        if line_length == 0:
            i += 4
        else:
            i += line_length
        if i >= len(data):
            break
    return lines


def build_lines_data(lines):
    """Build byte string from given lines to send to server."""
    result = []
    for line in lines:
        result.append('{:04x}'.format(len(line) + 5).encode())
        result.append(line)
        result.append(b'\n')
    result.append(b'0000')
    return b''.join(result)


def http_request(url, username, password, data=None):
    """Make an authenticated HTTP request to given URL (GET by default, POST
    if "data" is not None).
    """
    password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, url, username, password)
    auth_handler = urllib.request.HTTPBasicAuthHandler(password_manager)
    opener = urllib.request.build_opener(auth_handler)
    f = opener.open(url, data=data)
    return f.read()


def get_remote_master_hash(git_url, username, password):
    """Get commit hash of remote master branch, return SHA-1 hex string or
    None if no remote commits.
    """
    url = git_url + '/info/refs?service=git-receive-pack'
    response = http_request(url, username, password)
    lines = extract_lines(response)
    assert lines[0] == b'# service=git-receive-pack\n'
    assert lines[1] == b''
    if lines[2][:40] == b'0' * 40:
        return None
    master_sha1, master_ref = lines[2].split(b'\x00')[0].split()
    assert master_ref == b'refs/heads/master'
    assert len(master_sha1) == 40
    return master_sha1.decode()


def read_tree(sha1=None, data=None):
    """Read tree object with given SHA-1 (hex string) or data, and return list
    of (mode, path, sha1) tuples.
    """
    if sha1 is not None:
        obj_type, data = read_object(sha1)
        assert obj_type == 'tree'
    elif data is None:
        raise TypeError('must specify "sha1" or "data"')
    i = 0
    entries = []
    for _ in range(1000):
        end = data.find(b'\x00', i)
        if end == -1:
            break
        mode_str, path = data[i:end].decode().split()
        mode = int(mode_str, 8)
        digest = data[end + 1:end + 21]
        entries.append((mode, path, digest.hex()))
        i = end + 1 + 20
    return entries


def find_tree_objects(tree_sha1):
    """Return set of SHA-1 hashes of all objects in this tree (recursively),
    including the hash of the tree itself.
    """
    objects = {tree_sha1}
    for mode, path, sha1 in read_tree(sha1=tree_sha1):
        if stat.S_ISDIR(mode):
            objects.update(find_tree_objects(sha1))
        else:
            objects.add(sha1)
    return objects


def find_commit_objects(commit_sha1):
    """Return set of SHA-1 hashes of all objects in this commit (recursively),
    its tree, its parents, and the hash of the commit itself.
    """
    objects = {commit_sha1}
    obj_type, commit = read_object(commit_sha1)
    assert obj_type == 'commit'
    lines = commit.decode().splitlines()
    tree = next(l[5:45] for l in lines if l.startswith('tree '))
    objects.update(find_tree_objects(tree))
    parents = (l[7:47] for l in lines if l.startswith('parent '))
    for parent in parents:
        objects.update(find_commit_objects(parent))
    return objects


def find_missing_objects(local_sha1, remote_sha1):
    """Return set of SHA-1 hashes of objects in local commit that are missing
    at the remote (based on the given remote commit hash).
    """
    local_objects = find_commit_objects(local_sha1)
    if remote_sha1 is None:
        return local_objects
    remote_objects = find_commit_objects(remote_sha1)
    return local_objects - remote_objects


def encode_pack_object(obj):
    """Encode a single object for a pack file and return bytes (variable-
    length header followed by compressed data bytes).
    """
    obj_type, data = read_object(obj)
    type_num = ObjectType[obj_type].value
    size = len(data)
    byte = (type_num << 4) | (size & 0x0f)
    size >>= 4
    header = []
    while size:
        header.append(byte | 0x80)
        byte = size & 0x7f
        size >>= 7
    header.append(byte)
    return bytes(header) + zlib.compress(data)


def create_pack(objects):
    """Create pack file containing all objects in given given set of SHA-1
    hashes, return data bytes of full pack file.
    """
    header = struct.pack('!4sLL', b'PACK', 2, len(objects))
    body = b''.join(encode_pack_object(o) for o in sorted(objects))
    contents = header + body
    sha1 = hashlib.sha1(contents).digest()
    data = contents + sha1
    return data


def push(git_url): #, username=None, password=None):
    """Push master branch to given git repo URL.""" 
    if not check_if_repo_created():
        print('Repository has not been registered yet. Use\n\n`git create`\n\nbefore you push')
        return
    entries = read_index()
    print('Entries', read_index)
    files_to_push = []
    for entry in entries:
        print(entry)
        files_to_push.append(entry.path)
        #print('Path to file:', entry.path)
    print('Files to push', files_to_push)
    all_files_in_repo = []
    all_files_to_move = []
    for path, subdirs, files in os.walk('.'):
        for name in files:
            # we are excluding the objects files, since we are pushing the
            # files itself to ipfs. Therefore it doesn't make sense to
            # push the object files to. Additionaly we exclude all files
            # which are not indexed!
            full_path = os.path.join(path, name)
            print('Full path', full_path)
            if not path.startswith('./.git/objects') and (full_path in files_to_push or full_path.startswith('./.git')):
                all_files_in_repo.append(full_path)
            else:
               all_files_to_move.append(full_path)
               print(full_path[2:])
               #creates directory structure in tmp before the move
               os.makedirs(os.path.dirname('/tmp/' + full_path[2:]), exist_ok=True)
               # moves the file to tmp
               shutil.move(full_path[2:], '/tmp/' + full_path[2:])
               # TODO: do we need to delete the dirs at the source so that they won't get uploaded to ipfs?
    print('All files in repo', all_files_in_repo)
    print('All files to move', all_files_to_move)
    # IPFS STUFF START
    remote_cid_history = get_remote_cid_history()
    repo_name = read_repo_name()
    #client = ipfshttpclient.connect(IPFS_CONNECTION)
    client = ipfshttpclient.connect('/dns/ipfs.infura.io/tcp/5001/https')
    #here we are just getting the hash before pushing it to ipfs
    #before we push it to ipfs we will check if there is a contract
    #and if the CID's are differnt. If they are the same
    #we don't need to push
    res = client.add('../{:s}'.format(repo_name), recursive=True, only_hash=True)
    client.close()
    # IPFS STUFF STOP
    # we are pushing if remote
    if res[-1]['Hash'] not in remote_cid_history:
        print('Pushing content')
        res = client.add('../{:s}'.format(repo_name), recursive=True)
        push_new_cid(res[-1]['Hash'])
    else:
        print('There is nothing to push')
    for file in all_files_to_move:
        #print(file)
        # copying the files back to their source :)
        shutil.move('/tmp/' + file[2:], file[2:])
        # TODO: Do we need to remove the dirs? Should do that I guess
        
    ### ORIGINAL CODE
    #if username is None:
    #    username = os.environ['GIT_USERNAME']
    #if password is None:
    #    password = os.environ['GIT_PASSWORD']
    #remote_sha1 = get_remote_master_hash(git_url, username, password)
    #local_sha1 = get_local_master_hash()
    #missing = find_missing_objects(local_sha1, remote_sha1)
    #print('updating remote master from {} to {} ({} object{})'.format(
    #        remote_sha1 or 'no commits', local_sha1, len(missing),
    #        '' if len(missing) == 1 else 's'))
    #lines = ['{} {} refs/heads/master\x00 report-status'.format(
    #        remote_sha1 or ('0' * 40), local_sha1).encode()]
    #data = build_lines_data(lines) + create_pack(missing)
    #url = git_url + '/git-receive-pack'
    #response = http_request(url, username, password, data=data)
    #lines = extract_lines(response)
    #assert len(lines) >= 2, \
    #    'expected at least 2 lines, got {}'.format(len(lines))
    #assert lines[0] == b'unpack ok\n', \
    #    "expected line 1 b'unpack ok', got: {}".format(lines[0])
    #assert lines[1] == b'ok refs/heads/master\n', \
    #    "expected line 2 b'ok refs/heads/master\n', got: {}".format(lines[1])
    #return (remote_sha1, missing)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers(dest='command', metavar='command')
    sub_parsers.required = True

    sub_parser = sub_parsers.add_parser('add',
            help='add file(s) to index')
    sub_parser.add_argument('paths', nargs='+', metavar='path',
            help='path(s) of files to add')

    #sub_parser = sub_parsers.add_parser('cat-file',
            #help='display contents of object')
    #valid_modes = ['commit', 'tree', 'blob', 'size', 'type', 'pretty']
    #sub_parser.add_argument('mode', choices=valid_modes,
            #help='object type (commit, tree, blob) or display mode (size, '
                 #'type, pretty)')
    #sub_parser.add_argument('hash_prefix',
            #help='SHA-1 hash (or hash prefix) of object to display')

    sub_parser = sub_parsers.add_parser('commit',
            help='commit current state of index to master branch')
    sub_parser.add_argument('-a', '--author',
            help='commit author in format "A U Thor <author@example.com>" '
                 '(uses GIT_AUTHOR_NAME and GIT_AUTHOR_EMAIL environment '
                 'variables by default)')
    sub_parser.add_argument('-m', '--message', required=True,
            help='text of commit message')

    sub_parser = sub_parsers.add_parser('create',
            help='create your remote repository')
    
    sub_parser = sub_parsers.add_parser('clone',
            help='create your remote repository')    
    sub_parser.add_argument('name',
            help='name of repository to clone')    
    #sub_parser = sub_parsers.add_parser('diff',
            #help='show diff of files changed (between index and working '
                 #'copy)')

    #sub_parser = sub_parsers.add_parser('hash-object',
            #help='hash contents of given path (and optionally write to '
                 #'object store)')
    #sub_parser.add_argument('path',
            #help='path of file to hash')
    #sub_parser.add_argument('-t', choices=['commit', 'tree', 'blob'],
            #default='blob', dest='type',
            #help='type of object (default %(default)r)')
    #sub_parser.add_argument('-w', action='store_true', dest='write',
            #help='write object to object store (as well as printing hash)')

    sub_parser = sub_parsers.add_parser('init',
            help='initialize a new repo')
    sub_parser.add_argument('repo',
            nargs='?',
            default='.',
            help='directory name for new repo')

    #sub_parser = sub_parsers.add_parser('ls-files',
            #help='list files in index')
    #sub_parser.add_argument('-s', '--stage', action='store_true',
            #help='show object details (mode, hash, and stage number) in '
                 #'addition to path')

    sub_parser = sub_parsers.add_parser('push',
            help='push master branch to given git server URL')
    sub_parser.add_argument('git_url',
            help='URL of git repo, eg: https://github.com/benhoyt/pygit.git')
    #sub_parser.add_argument('-p', '--password',
            #help='password to use for authentication (uses GIT_PASSWORD '
                 #'environment variable by default)')
    #sub_parser.add_argument('-u', '--username',
            #help='username to use for authentication (uses GIT_USERNAME '
                 #'environment variable by default)')

    sub_parser = sub_parsers.add_parser('status',
            help='show status of working copy')

    args = parser.parse_args()
    if args.command == 'add':
        add(args.paths)
    elif args.command == 'cat-file':
        try:
            cat_file(args.mode, args.hash_prefix)
        except ValueError as error:
            print(error, file=sys.stderr)
            sys.exit(1)
    elif args.command == 'commit':
        commit(args.message, author=args.author)
    elif args.command == 'create':
        create()
    elif args.command == 'clone':
        clone(args.name)
    elif args.command == 'diff':
        diff()
    elif args.command == 'hash-object':
        sha1 = hash_object(read_file(args.path), args.type, write=args.write)
        print(sha1)
    elif args.command == 'init':
        init(args.repo)
    elif args.command == 'ls-files':
        ls_files(details=args.stage)
    elif args.command == 'push':
        push(args.git_url)#, username=args.username, password=args.password)
    elif args.command == 'status':
        status()
    else:
        assert False, 'unexpected command {!r}'.format(args.command)
