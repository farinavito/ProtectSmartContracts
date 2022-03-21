// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

/// @title A way to reduce the risk in smart contracts when one address is compromised.
/// @author Farina Vito

//import "https://github.com/farinavito/ProtectSmartContracts/blob/main/project/AddressProtector/contracts/protector.sol";
import "./../AddressProtector/build/contracts/AddressProtector";


contract ProtectorOwnerWaitingOwner is AddressProtector() {
    //maybe we should add functionality that you can't add protector for an owner

    /// @notice Storing the created candidates
    mapping (address => bool) public existingCandidates;

    /// @notice Only the protectorOwner can access
    modifier onlyprotectorOwner(){
        require(msg.sender == protectorOwner, "You are not the owner");
        _;
    }

    /// @notice Changing the owner and the waitingToBeOwner
    function changeOwner(address _nextInline) external {
        require(protectorWaitingToBeOwner == msg.sender, "You don't have permissions");
        require(protectorWaitingToBeOwner != _nextInline, "protectorWaitingToBeOwner can't be the same");
        require(candidatesVotes[_nextInline] == 5, "Not all protectors agree with this address");
        protectorOwner = protectorWaitingToBeOwner;
        protectorWaitingToBeOwner = _nextInline;
    }
    
    /// @notice Voting for candidates by protectors
    function voteCandidate(address _nextInLine, uint256 _id) external {
        require(protectors[_id].protectorAddress == msg.sender, "The id entered isn't equal to protector's id");
        require(alreadyVoted[msg.sender][_nextInLine] == false, "You have entered your vote");
        alreadyVoted[msg.sender][_nextInLine] = true;
        candidatesVotes[_nextInLine] += 1;
    }
    //add a require that number of votes cannot go under 0
    /// @notice remove vote by the protector from previously voted protectorWaitingToBeOwner
    function removeVote(address _nextInLine, uint256 _id) external {
        require(protectors[_id].protectorAddress == msg.sender, "You aren't a protector");
        require(alreadyVoted[msg.sender][_nextInLine] == true, "You haven't voted for this address");
        alreadyVoted[msg.sender][_nextInLine] = false;
        candidatesVotes[_nextInLine] -= 1;
    }
}