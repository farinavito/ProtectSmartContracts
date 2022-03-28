// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

/// @title A way to reduce the risk in smart contracts when one address is compromised.
/// @author Farina Vito

contract AddressProtector {

    /// @notice Adding votes for candidates by protectors
    mapping (address => mapping(address => bool)) public alreadyVoted;
    
    /// @notice Candidate for protectorWaitingToBeOwner
    mapping (address => uint256) public candidatesVotes;
        
    /// @notice Storing the owner's address
    address public smartContractOwner;

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
        smartContractOwner = _protectorOwner;
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
    
}