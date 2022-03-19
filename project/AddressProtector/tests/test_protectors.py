from itertools import chain
import pytest
import brownie
from brownie import *
from brownie import accounts
from brownie.network import rpc
from brownie.network.state import Chain

#addresses
protectorOwnerAddres = 1
protectorWaitingToBeOwnerAddress = 2
addressProtector1 = 3
addressProtector2 = 4
addressProtector3 = 5
addressProtector4 = 6
addressProtector5 = 7

@pytest.fixture()
def deploy(AddressProtector, module_isolation):
    return AddressProtector.deploy(accounts[1], accounts[2], accounts[3], accounts[4], accounts[5], accounts[6], accounts[7], {'from': accounts[0]})



'''TESTING CONSTRUCTOR INITIALIZATION'''



def test_protector1_initialization_id(deploy):
    '''testing protector 1 id when added to constructor'''
    assert deploy.protectors(1)[0] == 1

def test_protector1_initialization_address(deploy):
    '''testing protector 1 address when added to constructor'''
    assert deploy.protectors(1)[1] == accounts[addressProtector1]
@pytest.mark.aaa
def test_protector2_initialization_id(deploy):
    '''testing protector 2 address when added to constructor'''
    assert deploy.protectors(2)[0] == 2
@pytest.mark.aaa
def test_protector2_initialization_address(deploy):
    '''testing protector 2 address when added to constructor'''
    assert deploy.protectors(2)[1] == accounts[addressProtector2]