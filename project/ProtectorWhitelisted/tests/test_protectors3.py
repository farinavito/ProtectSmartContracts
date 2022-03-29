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
def deploy(ProtectorWhitelisted, module_isolation):
    return ProtectorWhitelisted.deploy({'from': accounts[0]})



'''TESTING ADDTOWHITELIST'''


@pytest.mark.aaa
@pytest.mark.parametrize("not_owner",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_addToWhitelist_onlyprotectorOwner(deploy, not_owner):
    '''checking if only the protectorOwner can access this function'''
    with brownie.reverts("You are not the owner"):
        deploy.addToWhitelist(accounts[8], {'from': accounts[not_owner]})
    
def test_addToWhitelist_whitelist_true(deploy):
    '''checking if the address is added to the whitelist'''
    deploy.addToWhitelist(accounts[8], {'from': accounts[protectorOwnerAddress]})
    assert deploy.whitelist(accounts[8]) == True

def test_addToWhitelist_uninitialized(deploy):
    '''checking if the whitelist returns false for not initialized address'''
    assert deploy.whitelist(accounts[8]) == False

def test_addToWhitelist_multipletimes(deploy):
    '''checking if the whitelist returns true when address added multiple times'''
    deploy.addToWhitelist(accounts[8], {'from': accounts[protectorOwnerAddress]})
    deploy.addToWhitelist(accounts[8], {'from': accounts[protectorOwnerAddress]})
    assert deploy.whitelist(accounts[8]) == True



'''TESTING REMOVEFROMWHITELIST'''


@pytest.mark.parametrize("not_owner",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeFromWhitelist_onlyprotectorOwner(deploy, not_owner):
    '''checking if only the protectorOwner can access this function'''
    assert deploy.removeFromWhitelist(accounts[8], {'from': accounts[not_owner]})
    '''
    with brownie.reverts("You are not the owner"):
        deploy.removeFromWhitelist(accounts[8], {'from': accounts[not_owner]})
    '''

def test_removeFromWhitelist_whitelist(deploy):
    '''checking if the address is added to the whitelist'''
    deploy.addToWhitelist(accounts[8], {'from': accounts[protectorOwnerAddress]})
    deploy.removeFromWhitelist(accounts[8], {'from': accounts[protectorOwnerAddress]})
    assert deploy.whitelist(accounts[8]) == False

def test_removeFromWhitelist_multipletimes(deploy):
    '''checking if the whitelist returns false when address removed multiple times'''
    deploy.removeFromWhitelist(accounts[8], {'from': accounts[protectorOwnerAddress]})
    deploy.removeFromWhitelist(accounts[8], {'from': accounts[protectorOwnerAddress]})
    assert deploy.whitelist(accounts[8]) == False