pragma solidity ^0.6.0;

import "github.com/OpenZeppelin/openzeppelin-solidity/contracts/access/Ownable.sol";

contract GitFactory is Ownable {
    GitRepository[] public GitRepositories;
    
    constructor() public Ownable() {}
    
    function createRepository(string memory name) public {
        GitRepository newGitRepo = new GitRepository(name, msg.sender);
        GitRepositories.push(newGitRepo);
    }
}

contract GitRepository is Ownable {
    // repository name
    string public repoName;
    
    string[] public cidHistory;
    // cid to newest repo
    string public headCid;
    
    constructor (string memory name, address owner) public Ownable() {
        repoName = name;
        transferOwnership(owner);
    }
    
    function push(string memory newCid) public onlyOwner {
        if (bytes(headCid).length != 0) {
            cidHistory.push(headCid);
        }
        headCid = newCid;
    }
}
