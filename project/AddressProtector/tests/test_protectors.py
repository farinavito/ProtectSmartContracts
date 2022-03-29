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



'''TESTING CONSTRUCTOR INITIALIZATION'''



def test_protectorOwner_address(deploy):
    '''testing protectorOwner address'''
    assert deploy.smartcontractOwner() == accounts[protectorOwnerAddress]

def test_protectorWaitingToBeOwnerAddress_address(deploy):
    '''testing protectorWaitingToBeOwnerAddress address'''
    assert deploy.protectorWaitingToBeOwner() == accounts[protectorWaitingToBeOwnerAddress]

def test_protector1_initialization_address(deploy):
    '''testing protector 1 address when added to constructor'''
    assert deploy.allprotectorsaddresses(addressProtector1 - 3) == accounts[addressProtector1]

def test_protector2_initialization_address(deploy):
    '''testing protector 2 address when added to constructor'''
    assert deploy.allprotectorsaddresses(addressProtector2 - 3) == accounts[addressProtector2]

def test_protector3_initialization_address(deploy):
    '''testing protector 3 address when added to constructor'''
    assert deploy.allprotectorsaddresses(addressProtector3 - 3) == accounts[addressProtector3]

def test_protector4_initialization_address(deploy):
    '''testing protector 4 address when added to constructor'''
    assert deploy.allprotectorsaddresses(addressProtector4 - 3) == accounts[addressProtector4]

def test_protector5_initialization_address(deploy):
    '''testing protector 5 address when added to constructor'''
    assert deploy.allprotectorsaddresses(addressProtector5 - 3) == accounts[addressProtector5]

def test_protector6_initialization_address(deploy):
    '''testing protector 6 address when added to constructor'''
    try:
         deploy.allprotectorsaddresses(6) == "0x0000000000000000000000000000000000000000"
    except Exception as e:
        assert e.message[50:] == ""

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_protector_alreadyVoted_owner_true(deploy, protector):
    '''checking if the the protector has initialized alreadyVoted to true'''
    assert deploy.alreadyVoted(accounts[protector], accounts[protectorWaitingToBeOwnerAddress]) == True

def test_alreadyvoted_protector6(deploy):
    '''check if protector6 will fail for already voted when initialize'''
    assert deploy.alreadyVoted(accounts[9], accounts[protectorWaitingToBeOwnerAddress]) == False

def test_alreadyvoted_protector7(deploy):
    '''check if protector7 will fail for already voted when initialize'''
    assert deploy.alreadyVoted(accounts[protectorOwnerAddress], accounts[protectorWaitingToBeOwnerAddress]) == False

def test_alreadyvoted_protector8(deploy):
    '''check if protector8 will fail for already voted when initialize'''
    assert deploy.alreadyVoted(accounts[protectorWaitingToBeOwnerAddress], accounts[protectorWaitingToBeOwnerAddress]) == False

def test_candidatesVotes_initialized_protectorWaitingToBeOwnerAddress_5(deploy):
    '''testing if protectorWaitingToBeOwnerAddress is initialized to 5'''
    assert deploy.candidatesVotes(accounts[protectorWaitingToBeOwnerAddress]) == 5

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_candidatesVotes_initialized_addressProtector(deploy, protector):
    '''testing if addressProtector is initialized to 0'''
    assert deploy.candidatesVotes(accounts[protector]) == 0

def test_candidatesVotes_initialized_protectorOwnerAddress(deploy):
    '''testing if protectorOwnerAddress is initialized to 0'''
    assert deploy.candidatesVotes(accounts[protectorOwnerAddress]) == 0


