// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

/// @title A way to reduce the risk in smart contracts when one address is compromised.
/// @author Farina Vito

contract Protector {

  struct Protectors{
    uint256 protectorId;
    address protectorAddress;    
  }

  mapping(address => mapping(address => bool)) alreadyVoted;

  /// @notice Used to increase the id of the agreements
  uint public numProtectors = 1;

  /// @notice A unique identifier of the protector
  mapping (uint256 => Protector) internal protectors;

  /// @notice Candidate for protectorWaitingToBeOwner
  mapping (address => uint256) candidates;
    
  /// @notice Storing the owner's address
  address internal protectortOwner;

  /// @notice Storing the next in line to be an owner
  address internal protectorWaitingToBeOwner;

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

    Protectors memory protectors = Protectors(numProtectors, _protector1);   
    /*
    Protectors storage newProtector = protectors[numProtectors];
    newProtector.protectorId = numProtectors;
    newProtector.protectorAddress = _protector1;
    */
    numProtectors++;
  
    /*
    protector1 = _protector1;
    protector2 = _protector2;
    protector3 = _protector3;
    protector4 = _protector4;
    protector5 = _protector5;
    */
  }

  modifier onlyprotectortOwner(){
      require(msg.sender == protectortOwner, "You are not the owner");
      _;
  }

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

  //create functionality that _nextInLine needs to be approved by multisig, if it's not, you can't change owner.
  /// @notice Changing the owner and the waitingToBeOwner
  function changeOwner(address _nextInline) external {
    require(protectorWaitingToBeOwner == msg.sender, "You don't have permissions");
    require(protectorWaitingToBeOwner != _nextInline, "protectorWaitingToBeOwner can't be the same");
    require(candidates[_nextInline] == 5, "Not all protectors agree with this address");
    protectortOwner = protectorWaitingToBeOwner;
    protectorWaitingToBeOwner = _nextInline;
  }

 
  function addCandidate(address _nextInLine, uint256 _id) external {
    require(protectors[_id].protectorAddress == msg.sender);
    candidates[_nextInLine] == 0;
  }


  function voteCandidate(address _nextInLine, uint256 _id) external {
    require(protectors[_id].protectorAddress == msg.sender);
    require(alreadyVoted[msg.sender][_nextInLine] == false, "You have entered your vote");
    alreadyVoted[msg.sender][_nextInLine] = true;
    candidates[_nextInLine] += 1;

  }

}