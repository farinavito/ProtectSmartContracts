import pytest
import brownie
from brownie import *
from brownie import accounts

#addresses
protectorOwnerAddress = 1
protectorWaitingToBeOwnerAddress = 2
addressProtector1 = 3
addressProtector2 = 4
addressProtector3 = 5
addressProtector4 = 6
addressProtector5 = 7

@pytest.fixture()
def deploy(AddressProtector, module_isolation):
    return AddressProtector.deploy(accounts[protectorOwnerAddress], accounts[protectorWaitingToBeOwnerAddress], accounts[addressProtector1], accounts[addressProtector2], accounts[addressProtector3], accounts[addressProtector4], accounts[addressProtector5], {'from': accounts[0]})



'''TESTING ADDTOWHITELIST'''



@pytest.mark.parametrize("not_owner",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_addToWhitelist_onlyprotectorOwner(deploy, not_owner):
    '''checking if only the protectorOwner can access this function'''
    assert deploy.addToWhitelist(accounts[8], {'from': accounts[not_owner]})
    '''
    with brownie.reverts("You are not the owner"):
        deploy.addToWhitelist(accounts[8], {'from': accounts[not_owner]})
    '''
    
def test_addToWhitelist_whitelist_true(deploy):
    '''checking if the address is added to the whitelist'''
    deploy.addToWhitelist(accounts[8], {'from': accounts[protectorOwnerAddress]})
    assert deploy.whitelist(accounts[8]) == True