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
    address internal protectortOwner;

    /// @notice Storing the next in line to be an owner
    address internal protectorWaitingToBeOwner;

    ///@notice Storing all protectors
    address[] internal allprotectorsaddresses;

    constructor (
        address _protectOwner,
        address _protectorWaitingToBeOwner, 
        address _protector1, 
        address _protector2, 
        address _protector3, 
        address _protector4, 
        address _protector5 
        ){
        protectortOwner = _protectOwner;
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

    /// @notice Only the protectortOwner can access
    modifier onlyprotectortOwner(){
        require(msg.sender == protectortOwner, "You are not the owner");
        _;
    }

    /// @notice Only the whitelisted address can access
    modifier onlyWhitelisted() {
        require(isWhitelisted(msg.sender), "You aren't whitelisted");
        _;
    }

    /// @notice Whitelisted accounts that can access withdrawal_amount_owner
    mapping(address => bool) public whitelist;

    /// @notice When an account is whitelisted
    event AddedToTheList(address account);

    /// @notice When an account is removed from whitelist
    event RemovedFromTheList(address account);

    /// @notice Adding address to the whitelist
    function addToWhitelist(address _address) external onlyprotectortOwner {
        whitelist[_address] = true;
        emit AddedToTheList(_address);
    }
    
    /// @notice Removing address from the whitelist
    function removedFromWhitelist(address _address) external onlyprotectortOwner {
        whitelist[_address] = false;
        emit RemovedFromTheList(_address);
    }

    /// @notice Changing the owner and the waitingToBeOwner
    function changeOwner(address _nextInline) external {
        require(protectorWaitingToBeOwner == msg.sender, "You don't have permissions");
        require(protectorWaitingToBeOwner != _nextInline, "protectorWaitingToBeOwner can't be the same");
        require(candidates[_nextInline] == 5, "Not all protectors agree with this address");
        protectortOwner = protectorWaitingToBeOwner;
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

    //maybe return all protectors -> make it public?


}