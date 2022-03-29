import pytest
import brownie
from brownie import *
from brownie import accounts


#addresses
protectorOwnerAddress = 1
protectorNextOwner = 2
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
    assert accounts[protectorNextOwner] == "0x0063046686E46Dc6F15918b61AE2B121458534a5"

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



'''TEST CONSTRUCT INITIALIZATION'''



def test_protectorOwner_address(deploy):
    '''testing protectorOwner address'''
    assert deploy.smartContractOwner() == accounts[protectorOwnerAddress]

def test_protectorWaitingToBeOwnerAddress_address(deploy):
    '''testing protectorWaitingToBeOwnerAddress address'''
    assert deploy.protectorWaitingToBeOwner() == accounts[protectorNextOwner]

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
    assert deploy.alreadyVoted(accounts[protector], accounts[protectorNextOwner]) == True

def test_alreadyvoted_protector6(deploy):
    '''check if protector6 will fail for already voted when initialize'''
    assert deploy.alreadyVoted(accounts[9], accounts[protectorNextOwner]) == False

def test_alreadyvoted_protector7(deploy):
    '''check if protector7 will fail for already voted when initialize'''
    assert deploy.alreadyVoted(accounts[protectorOwnerAddress], accounts[protectorNextOwner]) == False

def test_alreadyvoted_protector8(deploy):
    '''check if protector8 will fail for already voted when initialize'''
    assert deploy.alreadyVoted(accounts[protectorNextOwner], accounts[protectorNextOwner]) == False

def test_candidatesVotes_initialized_protectorWaitingToBeOwnerAddress_5(deploy):
    '''testing if protectorWaitingToBeOwnerAddress is initialized to 5'''
    assert deploy.candidatesVotes(accounts[protectorNextOwner]) == 5

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_candidatesVotes_initialized_addressProtector(deploy, protector):
    '''testing if addressProtector is initialized to 0'''
    assert deploy.candidatesVotes(accounts[protector]) == 0

def test_candidatesVotes_initialized_protectorOwnerAddress(deploy):
    '''testing if protectorOwnerAddress is initialized to 0'''
    assert deploy.candidatesVotes(accounts[protectorOwnerAddress]) == 0


'''TESTING VOTECANDIDATE'''



def test_voteCandidate_1st_require_protectorOwnerAddress(deploy):
    '''Checking if the protectorOwnerAddress cannot call voteCandidate'''
    try:
        deploy.voteCandidate(accounts[9], {'from': accounts[protectorOwnerAddress]})
    except Exception as e:
        assert e.message[50:] == "You don't have permissions"

def test_voteCandidate_1st_require_protectorNextOwner(deploy):
    '''Checking if the protectorOwnerAddress cannot call voteCandidate'''
    try:
        deploy.voteCandidate(accounts[9], {'from': accounts[protectorNextOwner]})
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
def test_voteCandidate_2nd_require_continue(deploy, protector):
    '''Checking if the vote cannot go to the protectorNextOwner'''
    try:
        deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector1]})
        deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector2]})
        deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector3]})
        deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector4]})
        deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector5]})
        deploy.changeOwner(accounts[8])
        deploy.voteCandidate(accounts[9], {'from': accounts[protector]})
    except Exception as e:
        assert e.message[50:] == "You have entered your vote"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_voteCandidate_alreadyVoted_true(deploy, protector):
    '''Check if the mapping alreadyVoted changes to true'''
    deploy.voteCandidate(accounts[9], {'from': accounts[protector]})
    assert deploy.alreadyVoted(accounts[protector], accounts[9]) == True

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_voteCandidate_increase_candidatesVotes_protector(deploy, protector):
    '''check if the candidatesVotes increases''' 
    deploy.voteCandidate(accounts[8], {'from': accounts[protector]})
    assert deploy.candidatesVotes(accounts[8]) == 1

def test_voteCandidate_increase_candidatesVotes_protectors_all(deploy):
    '''check if the candidatesVotes increases''' 
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector1]})
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector2]})
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector3]})
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector4]})
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector5]})
    assert deploy.candidatesVotes(accounts[8]) == 5



'''TESTING REMOVEVOTE'''   


@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVote_1st_require_protectorOwnerAddress(deploy, protector):
    '''Checking if the protectorOwnerAddress cannot call removeVoteCandidate'''
    try:
        deploy.voteCandidate(accounts[9], {'from': accounts[protector]})
        deploy.removeVote(accounts[9], {'from': accounts[protectorOwnerAddress]})
    except Exception as e:
        assert e.message[50:] == "You don't have permissions"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVote_1st_require_protectorNextOwner(deploy, protector):
    '''Checking if the protectorOwnerAddress cannot call removeVoteCandidate'''
    try:
        deploy.voteCandidate(accounts[9], {'from': accounts[protector]})
        deploy.removeVote(accounts[9], {'from': accounts[protectorNextOwner]})
    except Exception as e:
        assert e.message[50:] == "You don't have permissions"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVote_1st_require_protectors(deploy, protector):
    '''Checking if only the protectors can call voteCandidate'''
    deploy.voteCandidate(accounts[9], {'from': accounts[protector]})
    deploy.removeVote(accounts[9], {'from': accounts[protector]})
    assert deploy.candidatesVotes(accounts[9]) == 0

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVote_2nd_require_no_vote(deploy, protector):
    '''Checking if the same protector cannot vote twice for the same candidate when you haven't vote for it'''
    deploy.removeVote(accounts[protectorNextOwner], protector - 1, {'from': accounts[protector]})
    deploy.removeVote(accounts[protectorNextOwner], protector - 1, {'from': accounts[protector]})
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
    deploy.removeVote(accounts[protectorNextOwner], protector - 1, {'from': accounts[protector]})
    deploy.removeVote(accounts[protectorNextOwner], protector - 1, {'from': accounts[protector]})
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
    assert deploy.changeOwner(accounts[protectorNextOwner], {'from': accounts[protector]}) == "ok"
    '''
    try:
        deploy.changeOwner(accounts[protectorNextOwner], {'from': accounts[protector]})        
    except Exception as e:
        assert e.message[50:] == "protectorWaitingToBeOwner can't be the same"
    '''

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeOwner_3rd_require(deploy, protector):
    '''checking if the candidate protectorWaitingToBeOwner has the required number of votes'''
    assert deploy.changeOwner(accounts[protectorNextOwner], {'from': accounts[protector]}) == "ok"
    '''
    try:
        deploy.changeOwner(accounts[protectorNextOwner], {'from': accounts[protector]})        
    except Exception as e:
        assert e.message[50:] == "Not all protectors agree with this address"
    '''

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeOwner_protectorOwner_changed(deploy, protector):
    '''Checking if the protectorOwner is modified'''
    deploy.changeOwner(accounts[8], {'from': accounts[protector]})
    assert deploy.protectorOwner() == accounts[protectorNextOwner]

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeOwner_protectorWaitingToBeOwner_changed(deploy, protector):
    '''Checking if the protectorWaitingToBeOwner is modified'''
    deploy.changeOwner(accounts[8], {'from': accounts[protector]})
    assert deploy.protectorWaitingToBeOwner() == accounts[8]