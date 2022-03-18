// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

/// @title A way to reduce the risk in smart contracts when one address is compromised.
/// @author Farina Vito

import "https://github.com/farinavito/ProtectSmartContracts/blob/main/project/AddressProtector/contracts/protector.sol";

contract ProtectorOwnerWaitingOwner is AddressProtector() {

    /// @notice Candidate for protectorWaitingToBeOwner
    mapping (address => uint256) internal candidates;

    /// @notice Only the protectorOwner can access
    modifier onlyprotectorOwner(){
        require(msg.sender == protectorOwner, "You are not the owner");
        _;
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