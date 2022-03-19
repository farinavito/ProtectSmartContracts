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
    return AddressProtector.deploy(accounts[1], accounts[2], accounts[3], accounts[4], accounts[5], accounts[6], accounts[7], {'from': accounts[0]})



'''TESTING CHANGEOWNER'''


@pytest.mark.aaa
def test_changeOwner_1st_require(deploy):
    '''checking if the user has permissions to change the owner'''
    assert deploy.changeOwner(accounts[9], {'from': accounts[1]}) == "ok"
    '''
    try:
        deploy.changeOwner(accounts[9], {'from': accounts[1]})        
    except Exception as e:
        assert e.message[50:] == "The agreement's deadline has ended"
    '''
