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



'''TESTING VOTECANDIDATE'''



def test_voteCandidate_1st_require_protectorOwnerAddress(deploy):
    '''Checking if only the protector can access this function and not protectorOwnerAddress'''
    deploy.voteCandidate(accounts[9], 1, {'from': accounts[protectorOwnerAddress]})
    '''
    try:
        deploy.voteCandidate(accounts[9], 1, {'from': accounts[1]})
    except Exception as e:
        assert e.message[50:] == "The id entered isn't equal to protector's id"
    '''

def test_voteCandidate_1st_require_protectorWaitingToBeOwnerAddress(deploy):
    '''Checking if only the protector can access this function and not protectorWaitingToBeOwnerAddress'''
    deploy.voteCandidate(accounts[9], 1, {'from': accounts[addressProtector2]})
    '''
    try:
        deploy.voteCandidate(accounts[9], 1, {'from': accounts[1]})
    except Exception as e:
        assert e.message[50:] == "The id entered isn't equal to protector's id"
    '''

def test_voteCandidate_2nd_require_(deploy):
    '''Checking if the same protector cannot vote twice for the same candidate'''
    deploy.voteCandidate(accounts[9], 1, {'from': accounts[addressProtector1]})
    deploy.voteCandidate(accounts[9], 1, {'from': accounts[addressProtector1]})
    '''
    try:
        deploy.voteCandidate(accounts[9], 1, {'from': accounts[addressProtector1]})
        deploy.voteCandidate(accounts[9], 1, {'from': accounts[addressProtector1]})
    except Exception as e:
        assert e.message[50:] == "You have entered your vote"
    '''
def test_voteCandidate_alreadyVoted_true(deploy):
    '''Check if the mapping alreadyVoted changes to true'''
    deploy.voteCandidate(accounts[9], 1, {'from': accounts[addressProtector1]})
    assert deploy.alreadyVoted(accounts[addressProtector1], accounts[9]) == True

def test_voteCandidate_increase_candidatesVotes_protector1(deploy):
    '''check if the candidatesVotes increases''' 
    deploy.voteCandidate(accounts[8], 1, {'from': accounts[addressProtector1]})
    assert deploy.candidatesVotes(accounts[8]) == 1

def test_voteCandidate_increase_candidatesVotes_protector2(deploy):
    '''check if the candidatesVotes increases''' 
    deploy.voteCandidate(accounts[8], 2, {'from': accounts[addressProtector2]})
    assert deploy.candidatesVotes(accounts[8]) == 2

def test_voteCandidate_increase_candidatesVotes_protector3(deploy):
    '''check if the candidatesVotes increases''' 
    deploy.voteCandidate(accounts[8], 3, {'from': accounts[addressProtector3]})
    assert deploy.candidatesVotes(accounts[8]) == 3

def test_voteCandidate_increase_candidatesVotes_protector4(deploy):
    '''check if the candidatesVotes increases''' 
    deploy.voteCandidate(accounts[8], 4, {'from': accounts[addressProtector4]})
    assert deploy.candidatesVotes(accounts[8]) == 4

def test_voteCandidate_increase_candidatesVotes_protector5(deploy):
    '''check if the candidatesVotes increases''' 
    deploy.voteCandidate(accounts[8], 5, {'from': accounts[addressProtector5]})
    assert deploy.candidatesVotes(accounts[8]) == 5



'''TESTING REMOVEVOTE'''   



def test_removeVote_1st_require_protectorOwnerAddress(deploy):
    '''Checking if only the protector can access this function and not protectorOwnerAddress'''
    deploy.voteCandidate(accounts[9], 1, {'from': accounts[protectorOwnerAddress]})
    '''
    try:
        deploy.removeVote(accounts[9], 1, {'from': accounts[protectorOwnerAddress]})
    except Exception as e:
        assert e.message[50:] == "The id entered isn't equal to protector's id"
    '''

def test_removeVote_1st_require_protectorWaitingToBeOwnerAddress(deploy):
    '''Checking if only the protector can access this function and not protectorWaitingToBeOwnerAddress '''
    deploy.voteCandidate(accounts[9], 1, {'from': accounts[protectorWaitingToBeOwnerAddress]})
    '''
    try:
        deploy.removeVote(accounts[9], 1, {'from': accounts[protectorWaitingToBeOwnerAddress]})
    except Exception as e:
        assert e.message[50:] == "The id entered isn't equal to protector's id"
    '''

#check if you can remov more votes, maybe going negative?
#decrease to negative to user that isn't initialized
#check for initialized addresses, remove vote and vote
#remove vote if there already exists a candidate or it doesn't
#check if the candidate already exists

'''TESTING CHANGEOWNER'''


@pytest.mark.aaa
def test_changeOwner_1st_require(deploy):
    '''checking if the user has permissions to change the owner'''
    assert deploy.changeOwner(accounts[9], {'from': accounts[protectorOwnerAddress]}) == "ok"
    '''
    try:
        deploy.changeOwner(accounts[9], {'from': accounts[1]})        
    except Exception as e:
        assert e.message[50:] == "You don't have permissions"
    '''
@pytest.mark.aaa
def test_changeOwner_2nd_require(deploy):
    '''checking if the protectorWaitingToBeOwner is not the same as before'''
    assert deploy.changeOwner(accounts[protectorWaitingToBeOwnerAddress], {'from': accounts[addressProtector1]}) == "ok"
    '''
    try:
        deploy.changeOwner(accounts[protectorWaitingToBeOwnerAddress], {'from': accounts[3]})        
    except Exception as e:
        assert e.message[50:] == "protectorWaitingToBeOwner can't be the same"
    '''
@pytest.mark.aaa
def test_changeOwner_3rd_require(deploy):
    '''checking if the candidate protectorWaitingToBeOwner has the required number of votes'''
    assert deploy.changeOwner(accounts[protectorWaitingToBeOwnerAddress], {'from': accounts[addressProtector1]}) == "ok"
    '''
    try:
        deploy.changeOwner(accounts[protectorWaitingToBeOwnerAddress], {'from': accounts[3]})        
    except Exception as e:
        assert e.message[50:] == "Not all protectors agree with this address"
    '''