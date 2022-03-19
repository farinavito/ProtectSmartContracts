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
        
    /// @notice Storing the owner's address
    address public protectorOwner;

    /// @notice Storing the next in line to be an owner
    address public protectorWaitingToBeOwner;

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
        protectorWaitingToBeOwner = _protectorWaitingToBeOwner;

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
    
}