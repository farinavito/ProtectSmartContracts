// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

/// @title A way to reduce the risk in smart contracts when one address is compromised.
/// @author Farina Vito

contract AddressProtector {

    /// @notice Creating a protector
    struct protectorStruct{
        uint256 protectorId;
        address protectorAddress;    
    }

    /// @notice Adding votes for candidates by protectors
    mapping(address => mapping(address => bool)) public alreadyVoted;

    /// @notice A unique identifier of the protector
    mapping (uint256 => protectorStruct) public protectors;

    /// @notice Candidate for protectorWaitingToBeOwner
    mapping (address => uint256) internal candidates;
        
    /// @notice Storing the owner's address
    address internal protectorOwner;

    /// @notice Storing the next in line to be an owner
    address internal protectorWaitingToBeOwner;

    ///@notice Storing all protectors
    address[] internal allprotectorsaddresses;

    constructor (
        address _protectorOwner,
        address _protectorWaitingToBeOwner, 
        address _protector1, 
        address _protector2, 
        address _protector3, 
        address _protector4, 
        address _protector5 
        ){
        protectorOwner = _protectorOwner;
        protectorWaitingToBeOwner == _protectorWaitingToBeOwner;

        allprotectorsaddresses.push(_protector1);
        allprotectorsaddresses.push(_protector2);
        allprotectorsaddresses.push(_protector3);
        allprotectorsaddresses.push(_protector4);
        allprotectorsaddresses.push(_protector5);

        //initialize the protectors
        for (uint256 i = 1; i <= 5; i++){
            protectorStruct storage newProtector = protectors[i];
            newProtector.protectorId = i;
            newProtector.protectorAddress = allprotectorsaddresses[i - 1];
        }
    }

    /// @notice Only the protectorOwner can access
    modifier onlyprotectorOwner(){
        require(msg.sender == protectorOwner, "You are not the owner");
        _;
    }

    /// @notice Only the whitelisted address can access
    modifier onlyWhitelisted() {
        require(whitelist[msg.sender], "You aren't whitelisted");
        _;
    }

    /// @notice Whitelisted accounts that can access withdrawal_amount_owner
    mapping(address => bool) public whitelist;

    /// @notice Adding address to the whitelist
    //check if there already exists a whitelist address
    function addToWhitelist(address _address) external onlyprotectorOwner {
        whitelist[_address] = true;
    }
    
    /// @notice Removing address from the whitelist
    //check if there already exists a whitelist address
    function removedFromWhitelist(address _address) external onlyprotectorOwner {
        whitelist[_address] = false;
    }

    /// @notice Changing the owner and the waitingToBeOwner
    function changeOwner(address _nextInline) external {
        require(protectorWaitingToBeOwner == msg.sender, "You don't have permissions");
        require(protectorWaitingToBeOwner != _nextInline, "protectorWaitingToBeOwner can't be the same");
        require(candidates[_nextInline] == 5, "Not all protectors agree with this address");
        protectorOwner = protectorWaitingToBeOwner;
        protectorWaitingToBeOwner = _nextInline;
    }

    /// @notice Adding candidates by protectors
    function addCandidate(address _nextInLine, uint256 _id) external {
        require(protectors[_id].protectorAddress == msg.sender, "You aren't a protector");
        candidates[_nextInLine] = 0;
    }

    /// @notice Voting for candidates by protectors
    function voteCandidate(address _nextInLine, uint256 _id) external {
        require(protectors[_id].protectorAddress == msg.sender, "You aren't a protector");
        require(alreadyVoted[msg.sender][_nextInLine] == false, "You have entered your vote");
        alreadyVoted[msg.sender][_nextInLine] = true;
        candidates[_nextInLine] += 1;
    }

    /// @notice remove vote by the protector from previously voted protectorWaitingToBeOwner
    function removeVote(address _nextInLine, uint256 _id) external {
        require(protectors[_id].protectorAddress == msg.sender, "You aren't a protector");
        require(alreadyVoted[msg.sender][_nextInLine] == true, "You haven't voted for this address");
        alreadyVoted[msg.sender][_nextInLine] = false;
        candidates[_nextInLine] -= 1;
    }
    
}