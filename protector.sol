// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

/// @title A way to reduce the risk in smart contracts when one address is compromised.
/// @author Farina Vito

contract Protector {

    /// @notice Storing the owner's address
    address internal protectortOwner;

    /// @notice Storing the next in line to be an owner
    address protectorWaitingToBeOwner;

}