// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

/// @title A way to reduce the risk in smart contracts when one address is compromised.
/// @author Farina Vito

//import "https://github.com/farinavito/ProtectSmartContracts/blob/main/project/AddressProtector/contracts/protector.sol";
import "./../AddressProtector/build/contracts/protector.sol";


contract ProtectorOwnerWaitingOwner is AddressProtector() {
    //maybe we should add functionality that you can't add protector for an owner

    /// @notice Storing the created candidates
    mapping (address => bool) public existingCandidates;

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

    /// @notice Changing the owner and the waitingToBeOwner
    function changeOwner(address _nextInline) external {
        require(protectorWaitingToBeOwner == msg.sender, "You don't have permissions");
        require(protectorWaitingToBeOwner != _nextInline, "protectorWaitingToBeOwner can't be the same");
        require(candidatesVotes[_nextInline] == 5, "Not all protectors agree with this address");
        //reinitializing to 0
        smartContractOwner = protectorWaitingToBeOwner;
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
}