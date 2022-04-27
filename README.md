# ProtectSmartContracts
A way to reduce the risk in smart contracts when one address is compromised

VISUAL REPRESENTATION
---------------------

    protector 1 ---|
    protector 2 ---|
    protector 3 ---|----- protectorWaitingToBeOwner ---------- protectorOwner------------------------whitelistedAdresses
    protector 4 ---|      (can only change owner)     (can only add or removed from whitelist)       (do day to day jobs)
    protector 5 ---|



At the deployment we need to initialize:
    - protector 1
    - protector 2
    - protector 3
    - protector 4
    - protector 5
    - protectorWaitingToBeOwner
    - protectorOwner
    
FUNCTIONS OF DIFFERENT ADDRESS
------------------------------

    - protector 1-5 : They can add their vote for the the protectorWaitingToBeOwner which will become the protectorOwner after the owner will be changed. They can call voteCandidate and removeVote. 3 out of 5 protectors need to vote for a certain address to change.
    - protectorWaitingToBeOwner : If agreed, this address will become the smart contract owner. It can call changeOwner function
    - protectorOwner : It can only add or removed addresses from whitelist. It can call addToWhitelist and removedFromWhitelist function
    - whitelistedAddresses : This address should be used in the contract that inherits this one for day to day jobs (for example: as the require that only these addresses can access a certain function)
    
HOW TO INCLUDE THIS CONTRACT INTO YOUR's
----------------------------------------

In your smart contract write:

    AddressProtector public accessingProtectors;

    constructor(address _address) {
    accessingProtectors = AddressProtector(_address);
    }
    
Than you can use it as: 

    require(accessingProtectors.whitelist(msg.sender), "You aren't whitelisted");
