// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

/// @title A way to reduce the risk in smart contracts when one address is compromised.
/// @author Farina Vito

//what can I change?
// 2. for loop -> i something smaller than uint256 -> constructor, checkWhichProtector, returnProtector, changeOwner,
// 3. checkWhichProtector -> returns (uint256 _i), _i could be something smaller
// 4. changeOwner -> maybe only 3 out of 5?

contract AddressProtector {

    /// @notice Adding votes for candidates by protectors
    mapping (address => mapping(address => bool)) public alreadyVoted;
    
    /// @notice Candidate for protectorWaitingToBeOwner
    mapping (address => uint256) public candidatesVotes;

    /// @notice Whitelisted accounts that can access withdrawal_amount_owner
    mapping(address => bool) public whitelist;
        
    /// @notice Storing the owner's address
    address public smartcontractOwner;

    /// @notice Storing the next in line to be an owner
    address public protectorWaitingToBeOwner;

    ///@notice Storing all protectors
    address[] internal allprotectorsaddresses;

    /// @notice Emit all the addresses of the protectors
    event showAllProtectors(address indexed _address);


    constructor (
        address _protectorOwner,
        address _protectorWaitingToBeOwner, 
        address _protector1, 
        address _protector2, 
        address _protector3, 
        address _protector4, 
        address _protector5 
        ){
        smartcontractOwner = _protectorOwner;
        protectorWaitingToBeOwner = _protectorWaitingToBeOwner;

        allprotectorsaddresses.push(_protector1);
        allprotectorsaddresses.push(_protector2);
        allprotectorsaddresses.push(_protector3);
        allprotectorsaddresses.push(_protector4);
        allprotectorsaddresses.push(_protector5);

        //initialize the protectors
        for (uint256 i = 1; i <= 5; i++){
            candidatesVotes[protectorWaitingToBeOwner] += 1;
            alreadyVoted[allprotectorsaddresses[i - 1]][protectorWaitingToBeOwner] = true;
        }
    }

    /// @notice Checking if the input address is the protector
    function checkWhichProtector(address _address) internal view returns(uint256 _i){
        for (uint256 i = 0; i < 5; i++){
            if (allprotectorsaddresses[i] == _address){
                return i;
            } else if (i != 4){
                continue;
            } else {
                revert("You don't have permissions");
            }
        }
    }

    /// @notice Returning all addresses of protectors
    function returnProtectors() external {
        for (uint256 i = 0; i < 5; i++){
            emit showAllProtectors(allprotectorsaddresses[i]);
        }
    }

    /// @notice Changing the owner and the waitingToBeOwner
    function changeOwner(address _nextInline) external {
        require(protectorWaitingToBeOwner == msg.sender, "You don't have permissions");
        require(candidatesVotes[_nextInline] == 5, "Not all protectors agree with this address");
        //reinitializing to 0
        candidatesVotes[smartcontractOwner] = 0;
        for (uint256 i = 0; i < 5; i++){
            alreadyVoted[allprotectorsaddresses[i]][smartcontractOwner] = false;
        }

        smartcontractOwner = protectorWaitingToBeOwner;
        protectorWaitingToBeOwner = _nextInline;
    }
    
    /// @notice Voting for candidates by protectors
    function voteCandidate(address _nextInLine) external {
        checkWhichProtector(msg.sender);
        require(alreadyVoted[msg.sender][_nextInLine] == false, "You have entered your vote");
        alreadyVoted[msg.sender][_nextInLine] = true;
        candidatesVotes[_nextInLine] += 1;
    }

    /// @notice remove vote by the protector from previously voted protectorWaitingToBeOwner
    function removeVote(address _nextInLine) external {
        checkWhichProtector(msg.sender);
        require(alreadyVoted[msg.sender][_nextInLine] == true, "You haven't voted for this address");
        alreadyVoted[msg.sender][_nextInLine] = false;
        candidatesVotes[_nextInLine] -= 1;
    }

    /// @notice Only the whitelisted address can access
    modifier onlyWhitelisted() {
        require(whitelist[msg.sender], "You aren't whitelisted");
        _;
    }

    /// @notice Only the protectorOwner can access
    modifier onlyprotectorOwner(){
        require(msg.sender == smartcontractOwner, "You are not the owner");
        _;
    }

    /// @notice Adding address to the whitelist
    function addToWhitelist(address _address) external onlyprotectorOwner {
        whitelist[_address] = true;
    }
    
    /// @notice Removing address from the whitelist
    function removedFromWhitelist(address _address) external onlyprotectorOwner {
        whitelist[_address] = false;
    }
    
}