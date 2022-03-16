// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

/// @title A way to reduce the risk in smart contracts when one address is compromised.
/// @author Farina Vito

contract Protector {

    address protector1;
    address protector2;
    address protector3;
    address protector4;
    address protector5;
    
    /// @notice Storing the owner's address
    address internal protectortOwner;

    /// @notice Storing the next in line to be an owner
    address internal protectorWaitingToBeOwner;

    constructor (
        address _protectorWaitingToBeOwner, 
        address _protector1, 
        address _protector2, 
        address _protector3, 
        address _protector4, 
        address _protector5 
        ){
      protectortOwner = msg.sender;
      protectorWaitingToBeOwner == _protectorWaitingToBeOwner;
      protector1 = _protector1;
      protector2 = _protector2;
      protector3 = _protector3;
      protector4 = _protector4;
      protector5 = _protector5;
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
  function changeOwner(addres _nextInline) external {
    require(waitingToBeOwner == msg.sender, "You don't have permissions");
    require(waitingToBeOwner != _nextInline);
    owner = waitingToBeOwner;
    waitingToBeOwner = _nextInline;
  }

}