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



'''TESTING VOTECANDIDATE'''



def test_voteCandidate_1st_require_protectorOwnerAddress(deploy):
    '''Checking if only the protector can access this function and not protectorOwnerAddress'''
    deploy.voteCandidate(accounts[9], 1, {'from': accounts[1]})
    '''
    try:
        deploy.voteCandidate(accounts[9], 1, {'from': accounts[1]})
    except Exception as e:
        assert e.message[50:] == "The id entered isn't equal to protector's id"
    '''

def test_voteCandidate_1st_require_protectorWaitingToBeOwnerAddress(deploy):
    '''Checking if only the protector can access this function and not protectorWaitingToBeOwnerAddress'''
    deploy.voteCandidate(accounts[9], 1, {'from': accounts[2]})
    '''
    try:
        deploy.voteCandidate(accounts[9], 1, {'from': accounts[1]})
    except Exception as e:
        assert e.message[50:] == "The id entered isn't equal to protector's id"
    '''

def test_voteCandidate_2nd_require_(deploy):
    '''Checking if the same protector cannot vote twice for the same candidate'''
    deploy.voteCandidate(accounts[9], 1, {'from': accounts[3]})
    deploy.voteCandidate(accounts[9], 1, {'from': accounts[3]})
    '''
    try:
        deploy.voteCandidate(accounts[9], 1, {'from': accounts[3]})
        deploy.voteCandidate(accounts[9], 1, {'from': accounts[3]})
    except Exception as e:
        assert e.message[50:] == "You have entered your vote"
    '''
def test_voteCandidate_alreadyVoted_true(deploy):
    '''Check if the mapping alreadyVoted changes to true'''
    deploy.voteCandidate(accounts[9], 1, {'from': accounts[3]})
    assert deploy.alreadyVoted(accounts[addressProtector1], accounts[9]) == True

def test_voteCandidate_increase_candidatesVotes(deploy):
    '''check if the candidatesVotes increases''' 
    deploy.voteCandidate(accounts[8], 1, {'from': accounts[3]})
    assert deploy.candidatesVotes(accounts[8]) == 1



'''TESTING REMOVEVOTE'''   



def test_removeVote_1st_require_protectorOwnerAddress(deploy):
    '''Checking if only the protector can access this function and not protectorOwnerAddress'''

def test_removeVote_1st_require_protectorWaitingToBeOwnerAddress(deploy):
    '''Checking if only the protector can access this function and not protectorWaitingToBeOwnerAddress '''

'''TESTING CHANGEOWNER'''


@pytest.mark.aaa
def test_changeOwner_1st_require(deploy):
    '''checking if the user has permissions to change the owner'''
    assert deploy.changeOwner(accounts[9], {'from': accounts[1]}) == "ok"
    '''
    try:
        deploy.changeOwner(accounts[9], {'from': accounts[1]})        
    except Exception as e:
        assert e.message[50:] == "You don't have permissions"
    '''
@pytest.mark.aaa
def test_changeOwner_2nd_require(deploy):
    '''checking if the protectorWaitingToBeOwner is not the same as before'''
    assert deploy.changeOwner(accounts[protectorWaitingToBeOwnerAddress], {'from': accounts[3]}) == "ok"
    '''
    try:
        deploy.changeOwner(accounts[protectorWaitingToBeOwnerAddress], {'from': accounts[3]})        
    except Exception as e:
        assert e.message[50:] == "protectorWaitingToBeOwner can't be the same"
    '''
@pytest.mark.aaa
def test_changeOwner_3rd_require(deploy):
    '''checking if the candidate protectorWaitingToBeOwner has the required number of votes'''
    assert deploy.changeOwner(accounts[protectorWaitingToBeOwnerAddress], {'from': accounts[3]}) == "ok"
    '''
    try:
        deploy.changeOwner(accounts[protectorWaitingToBeOwnerAddress], {'from': accounts[3]})        
    except Exception as e:
        assert e.message[50:] == "Not all protectors agree with this address"
    '''