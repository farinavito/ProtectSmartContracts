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
def deploy(ProtectorOwnerWaitingOwner, module_isolation):
    return ProtectorOwnerWaitingOwner.deploy({'from': accounts[0]})

def test_acc1():
    assert accounts[protectorOwnerAddress] == "0x33A4622B82D4c04a53e170c638B944ce27cffce3"

def test_acc2():
    assert accounts[protectorWaitingToBeOwnerAddress] == "0x0063046686E46Dc6F15918b61AE2B121458534a5"

def test_acc3():
    assert accounts[addressProtector1] == "0x21b42413bA931038f35e7A5224FaDb065d297Ba3"

def test_acc4():
    assert accounts[addressProtector2] == "0x46C0a5326E643E4f71D3149d50B48216e174Ae84"

def test_acc5():
    assert accounts[addressProtector3] == "0x807c47A89F720fe4Ee9b8343c286Fc886f43191b"

def test_acc6():
    assert accounts[addressProtector4] == "0x844ec86426F076647A5362706a04570A5965473B"

def test_acc7():
    assert accounts[addressProtector5] == "0x23BB2Bb6c340D4C91cAa478EdF6593fC5c4a6d4B"


'''TESTING VOTECANDIDATE'''



def test_voteCandidate_1st_require_protectorOwnerAddress(deploy):
    '''Checking if the protectorOwnerAddress cannot call voteCandidate'''
    try:
        deploy.voteCandidate(accounts[9], {'from': accounts[protectorOwnerAddress]})
    except Exception as e:
        assert e.message[50:] == "You don't have permissions"

def test_voteCandidate_1st_require_protectorWaitingToBeOwnerAddress(deploy):
    '''Checking if the protectorOwnerAddress cannot call voteCandidate'''
    try:
        deploy.voteCandidate(accounts[9], {'from': accounts[protectorWaitingToBeOwnerAddress]})
    except Exception as e:
        assert e.message[50:] == "You don't have permissions"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_voteCandidate_1st_require_protectors(deploy, protector):
    '''Checking if only the protectors can call voteCandidate'''
    deploy.voteCandidate(accounts[9], {'from': accounts[protector]})
    assert deploy.candidatesVotes(accounts[9]) == 1

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_voteCandidate_2nd_require_(deploy, protector):
    '''Checking if the same protector cannot vote twice for the same candidate'''
    try:
        deploy.voteCandidate(accounts[9], {'from': accounts[protector]})
        deploy.voteCandidate(accounts[9], {'from': accounts[protector]})
    except Exception as e:
        assert e.message[50:] == "You have entered your vote"
 
@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_voteCandidate_alreadyVoted_true(deploy, protector):
    '''Check if the mapping alreadyVoted changes to true'''
    deploy.voteCandidate(accounts[9], protector - 1, {'from': accounts[protector]})
    assert deploy.alreadyVoted(accounts[protector], accounts[9]) == True

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_voteCandidate_increase_candidatesVotes_protector(deploy, protector):
    '''check if the candidatesVotes increases''' 
    deploy.voteCandidate(accounts[8], protector - 1, {'from': accounts[protector]})
    assert deploy.candidatesVotes(accounts[8]) == 1

def test_voteCandidate_increase_candidatesVotes_protectors_all(deploy):
    '''check if the candidatesVotes increases''' 
    deploy.voteCandidate(accounts[8], addressProtector1, {'from': accounts[addressProtector1]})
    deploy.voteCandidate(accounts[8], addressProtector2, {'from': accounts[addressProtector2]})
    deploy.voteCandidate(accounts[8], addressProtector3, {'from': accounts[addressProtector3]})
    deploy.voteCandidate(accounts[8], addressProtector4, {'from': accounts[addressProtector4]})
    deploy.voteCandidate(accounts[8], addressProtector5, {'from': accounts[addressProtector5]})
    assert deploy.candidatesVotes(accounts[8]) == 5



'''TESTING REMOVEVOTE'''   



def test_removeVote_1st_require_protectorOwnerAddress(deploy):
    '''Checking if only the protector can access this function and not protectorOwnerAddress'''
    deploy.removeVote(accounts[9], 1, {'from': accounts[protectorOwnerAddress]})
    '''
    try:
        deploy.removeVote(accounts[9], 1, {'from': accounts[protectorOwnerAddress]})
    except Exception as e:
        assert e.message[50:] == "The id entered isn't equal to protector's id"
    '''

def test_removeVote_1st_require_protectorWaitingToBeOwnerAddress(deploy):
    '''Checking if only the protector can access this function and not protectorWaitingToBeOwnerAddress '''
    deploy.removeVote(accounts[9], 1, {'from': accounts[protectorWaitingToBeOwnerAddress]})
    '''
    try:
        deploy.removeVote(accounts[9], 1, {'from': accounts[protectorWaitingToBeOwnerAddress]})
    except Exception as e:
        assert e.message[50:] == "The id entered isn't equal to protector's id"

    '''
@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVote_2nd_require_no_vote(deploy, protector):
    '''Checking if the same protector cannot vote twice for the same candidate when you haven't vote for it'''
    deploy.removeVote(accounts[protectorWaitingToBeOwnerAddress], protector - 1, {'from': accounts[protector]})
    deploy.removeVote(accounts[protectorWaitingToBeOwnerAddress], protector - 1, {'from': accounts[protector]})
    '''
    try:
        deploy.removeVote(accounts[9], protector - 1, {'from': accounts[protector]})
        deploy.removeVote(accounts[9], protector - 1, {'from': accounts[protector]})
    except Exception as e:
        assert e.message[50:] == "You have entered your vote"
    '''

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVote_2nd_require_prior_vote(deploy, protector):
    '''Checking if the same protector cannot vote twice for the same candidate'''
    deploy.voteCandidate(accounts[9], protector - 1, {'from': accounts[protector]})
    deploy.removeVote(accounts[protectorWaitingToBeOwnerAddress], protector - 1, {'from': accounts[protector]})
    deploy.removeVote(accounts[protectorWaitingToBeOwnerAddress], protector - 1, {'from': accounts[protector]})
    '''
    try:
        deploy.voteCandidate(accounts[9], protector - 1, {'from': accounts[protector]})
        deploy.removeVote(accounts[9], protector - 1, {'from': accounts[protector]})
        deploy.removeVote(accounts[9], protector - 1, {'from': accounts[protector]})
    except Exception as e:
        assert e.message[50:] == "You have entered your vote"
    '''
@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVote_alreadyVoted(deploy, protector):
    '''check if alreadyVoted returns false after the protector removes its vote'''
    deploy.voteCandidate(accounts[9], protector - 1, {'from': accounts[protector]})
    deploy.removeVote(accounts[9], protector - 1, {'from': accounts[protector]})
    assert deploy.alreadyVoted(accounts[protector], accounts[9]) == False

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_voteCandidate_alreadyVoted_after_remove_all_protectors(deploy, protector):
    '''check if alreadyVoted returns false after the protector removes its vote'''
    deploy.voteCandidate(accounts[9], 1, {'from': accounts[addressProtector1]})
    deploy.voteCandidate(accounts[9], 2, {'from': accounts[addressProtector2]})
    deploy.voteCandidate(accounts[9], 3, {'from': accounts[addressProtector3]})
    deploy.voteCandidate(accounts[9], 4, {'from': accounts[addressProtector4]})
    deploy.voteCandidate(accounts[9], 5, {'from': accounts[addressProtector5]})
    deploy.removeVote(accounts[9], 1, {'from': accounts[addressProtector1]})
    deploy.removeVote(accounts[9], 2, {'from': accounts[addressProtector2]})
    deploy.removeVote(accounts[9], 3, {'from': accounts[addressProtector3]})
    deploy.removeVote(accounts[9], 4, {'from': accounts[addressProtector4]})
    deploy.removeVote(accounts[9], 5, {'from': accounts[addressProtector5]})
    assert deploy.alreadyVoted(accounts[protector], accounts[9]) == False

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_voteCandidate_candidates_decrement_protector(deploy, protector):
    '''Checking if the candidates number decreases after the protector submits its removal vote'''
    deploy.voteCandidate(accounts[9], protector - 1, {'from': accounts[protector]})
    deploy.removeVote(accounts[9], protector - 1, {'from': accounts[protector]})
    assert deploy.candidates(accounts[9]) == 0

def test_voteCandidate_candidates_decrement_all_protectors(deploy):
    '''Checking if the candidates number decreases after the protector submits its removal vote'''
    deploy.voteCandidate(accounts[9], 1, {'from': accounts[addressProtector1]})
    deploy.voteCandidate(accounts[9], 2, {'from': accounts[addressProtector2]})
    deploy.voteCandidate(accounts[9], 3, {'from': accounts[addressProtector3]})
    deploy.voteCandidate(accounts[9], 4, {'from': accounts[addressProtector4]})
    deploy.voteCandidate(accounts[9], 5, {'from': accounts[addressProtector5]})
    deploy.removeVote(accounts[9], 1, {'from': accounts[addressProtector1]})
    deploy.removeVote(accounts[9], 2, {'from': accounts[addressProtector2]})
    deploy.removeVote(accounts[9], 3, {'from': accounts[addressProtector3]})
    deploy.removeVote(accounts[9], 4, {'from': accounts[addressProtector4]})
    deploy.removeVote(accounts[9], 5, {'from': accounts[addressProtector5]})
    assert deploy.candidates(accounts[9]) == 0



'''TESTING CHANGEOWNER'''



def test_changeOwner_1st_require(deploy):
    '''checking if the user has permissions to change the owner'''
    assert deploy.changeOwner(accounts[9], {'from': accounts[protectorOwnerAddress]}) == "ok"
    '''
    try:
        deploy.changeOwner(accounts[9], {'from': accounts[1]})        
    except Exception as e:
        assert e.message[50:] == "You don't have permissions"
    '''
@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeOwner_2nd_require(deploy, protector):
    '''checking if the protectorWaitingToBeOwner is not the same as before'''
    assert deploy.changeOwner(accounts[protectorWaitingToBeOwnerAddress], {'from': accounts[protector]}) == "ok"
    '''
    try:
        deploy.changeOwner(accounts[protectorWaitingToBeOwnerAddress], {'from': accounts[protector]})        
    except Exception as e:
        assert e.message[50:] == "protectorWaitingToBeOwner can't be the same"
    '''

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeOwner_3rd_require(deploy, protector):
    '''checking if the candidate protectorWaitingToBeOwner has the required number of votes'''
    assert deploy.changeOwner(accounts[protectorWaitingToBeOwnerAddress], {'from': accounts[protector]}) == "ok"
    '''
    try:
        deploy.changeOwner(accounts[protectorWaitingToBeOwnerAddress], {'from': accounts[protector]})        
    except Exception as e:
        assert e.message[50:] == "Not all protectors agree with this address"
    '''

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeOwner_protectorOwner_changed(deploy, protector):
    '''Checking if the protectorOwner is modified'''
    deploy.changeOwner(accounts[8], {'from': accounts[protector]})
    assert deploy.protectorOwner() == accounts[protectorWaitingToBeOwnerAddress]

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeOwner_protectorWaitingToBeOwner_changed(deploy, protector):
    '''Checking if the protectorWaitingToBeOwner is modified'''
    deploy.changeOwner(accounts[8], {'from': accounts[protector]})
    assert deploy.protectorWaitingToBeOwner() == accounts[8]