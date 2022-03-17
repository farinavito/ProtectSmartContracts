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
    //change to internal
    mapping(address => mapping(address => bool)) public alreadyVoted;

    /// @notice Used to increase the id of the agreements
    uint public numProtectors = 1;

    /// @notice A unique identifier of the protector
    //change back to internal
    mapping (uint256 => protectorStruct) public protectors;

    /// @notice Candidate for protectorWaitingToBeOwner
    //change to internal
    mapping (address => uint256) public candidates;
        
    /// @notice Storing the owner's address
    address internal protectortOwner;

    /// @notice Storing the next in line to be an owner
    address internal protectorWaitingToBeOwner;

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

        //allprotectorsaddresses.push(_protector1, _protector2, _protector3, _protector4, _protector5);
        allprotectorsaddresses.push(_protector1);
        allprotectorsaddresses.push(_protector2);
        allprotectorsaddresses.push(_protector3);
        allprotectorsaddresses.push(_protector4);
        allprotectorsaddresses.push(_protector5);

        for (uint256 i = 1; i <= 5; i++){
            protectorStruct storage newProtector = protectors[i];
            newProtector.protectorId = numProtectors;
            newProtector.protectorAddress = allprotectorsaddresses[i - 1];
            alreadyVoted[allprotectorsaddresses[i - 1]][protectorWaitingToBeOwner] = true;
        }
        /*
        protectorStruct storage newProtector = protectors[numProtectors];
        //initialize 1st protector
        newProtector.protectorId = numProtectors;
        newProtector.protectorAddress = _protector1;
        alreadyVoted[_protector1][protectorWaitingToBeOwner] = true; 

        //initialize 2nd protector
        numProtectors++;
        newProtector.protectorId = numProtectors;
        newProtector.protectorAddress = _protector2;
       
        //initialize 3rd protector
        numProtectors++;
        newProtector.protectorId = numProtectors;
        newProtector.protectorAddress = _protector3;
        alreadyVoted[_protector3][protectorWaitingToBeOwner] = true;

        //initialize 4th protector
        numProtectors++;
        newProtector.protectorId = numProtectors;
        newProtector.protectorAddress = _protector4;
        alreadyVoted[_protector4][protectorWaitingToBeOwner] = true; 

        //initialize 5th protector
        numProtectors++;
        newProtector.protectorId = numProtectors;
        newProtector.protectorAddress = _protector5;
        alreadyVoted[_protector5][protectorWaitingToBeOwner] = true; 
        */
        //initialized candidate votes to 5
        candidates[protectorWaitingToBeOwner] = 5;

        
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
    mapping(address => bool) internal whitelist;

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
    
    /// @notice Checking if the address is whitelisted
    function isWhitelisted(address _address) internal view returns(bool) {
        return whitelist[_address];
    }

    /// @notice Checking if the address is whitelisted by the same address
    function isWhitelistedExternal(address _address) external view onlyWhitelisted returns(bool) {
        return whitelist[_address];
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

    /// JUST FOR TESTING
    function showProtectorAddress( uint256 _id) external view returns(address){
        return protectors[_id].protectorAddress;
    } 

    /// JUST FOR TESTING
    function setVote( uint256 _id, address _nextInLine) external {
        alreadyVoted[protectors[_id].protectorAddress][_nextInLine] = true;
    } 

}