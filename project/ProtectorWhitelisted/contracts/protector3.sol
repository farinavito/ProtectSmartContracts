// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

/// @title A way to reduce the risk in smart contracts when one address is compromised.
/// @author Farina Vito

//import "https://github.com/farinavito/ProtectSmartContracts/blob/main/project/ProtectorOwnerAndWaitingOwner/contracts/protector2.sol";
import "farinavito/ProtectSmartContracts@1.0.0/project/ProtectorOwnerAndWaitingOwner/contracts/protector2.sol";

contract ProtectorWhitelisted is ProtectorOwnerWaitingOwner(){
    
    /// @notice Only the whitelisted address can access
    modifier onlyWhitelisted() {
        require(whitelist[msg.sender], "You aren't whitelisted");
        _;
    }

    /// @notice Only the protectorOwner can access
    modifier onlyprotectorOwner(){
        require(msg.sender == smartContractOwner, "You are not the owner");
        _;
    }

    /// @notice Whitelisted accounts that can access withdrawal_amount_owner
    mapping(address => bool) public whitelist;

    /// @notice Adding address to the whitelist
    function addToWhitelist(address _address) external onlyprotectorOwner {
        whitelist[_address] = true;
    }
    
    /// @notice Removing address from the whitelist
    function removedFromWhitelist(address _address) external onlyprotectorOwner {
        whitelist[_address] = false;
    }
}