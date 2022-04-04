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
        deploy.changeOwner(accounts[9], {'from': accounts[protectorNextOwner]})
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
def test_removeVote_2nd_require_(deploy, protector):
    '''Checking if the same protector cannot vote twice for the same candidate'''
    try:
        deploy.voteCandidate(accounts[9], {'from': accounts[protector]})
        deploy.removeVote(accounts[9], {'from': accounts[protector]})
        deploy.removeVote(accounts[9], {'from': accounts[protector]})
    except Exception as e:
        assert e.message[50:] == "You haven't voted for this address"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVote_2nd_require_continue(deploy, protector):
    '''Checking if the vote cannot go to the protectorNextOwner'''
    try:
        deploy.removeVote(accounts[9], {'from': accounts[protector]})
    except Exception as e:
        assert e.message[50:] == "You haven't voted for this address"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVote_alreadyVoted(deploy, protector):
    '''check if alreadyVoted returns false after the protector removes its vote'''
    deploy.voteCandidate(accounts[9], {'from': accounts[protector]})
    deploy.removeVote(accounts[9], {'from': accounts[protector]})
    assert deploy.alreadyVoted(accounts[protector], accounts[9]) == False

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVote_alreadyVoted_after_remove_all_protectors(deploy, protector):
    '''check if alreadyVoted returns false after the protector removes its vote'''
    deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector1]})
    deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector2]})
    deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector3]})
    deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector4]})
    deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector5]})
    deploy.removeVote(accounts[9], {'from': accounts[addressProtector1]})
    deploy.removeVote(accounts[9], {'from': accounts[addressProtector2]})
    deploy.removeVote(accounts[9], {'from': accounts[addressProtector3]})
    deploy.removeVote(accounts[9], {'from': accounts[addressProtector4]})
    deploy.removeVote(accounts[9], {'from': accounts[addressProtector5]})
    assert deploy.alreadyVoted(accounts[protector], accounts[9]) == False

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_removeVote_candidates_decrement_protector(deploy, protector):
    '''Checking if the candidates number decreases after the protector submits its removal vote'''
    deploy.voteCandidate(accounts[9], {'from': accounts[protector]})
    deploy.removeVote(accounts[9], {'from': accounts[protector]})
    assert deploy.candidatesVotes(accounts[9]) == 0

def test_removeVote_candidates_decrement_all_protectors(deploy):
    '''Checking if the candidates number decreases after the protector submits its removal vote'''
    deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector1]})
    deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector2]})
    deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector3]})
    deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector4]})
    deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector5]})
    deploy.removeVote(accounts[9], {'from': accounts[addressProtector1]})
    deploy.removeVote(accounts[9], {'from': accounts[addressProtector2]})
    deploy.removeVote(accounts[9], {'from': accounts[addressProtector3]})
    deploy.removeVote(accounts[9], {'from': accounts[addressProtector4]})
    deploy.removeVote(accounts[9], {'from': accounts[addressProtector5]})
    assert deploy.candidatesVotes(accounts[9]) == 0



'''TESTING CHANGEOWNER'''



@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5, protectorOwnerAddress])
def test_changeOwner_1st_require_false(deploy, protector):
    '''checking if these users don't have permissions to change the owner'''
    try:
        deploy.changeOwner(accounts[9], {'from': accounts[protector]})        
    except Exception as e:
        assert e.message[50:] == "You don't have permissions"

def test_changeOwner_1st_require_true(deploy):
    '''checking if the protectorNextOwner can access this function'''
    try:
        deploy.changeOwner(accounts[9],  {'from': accounts[protectorNextOwner]})
    except Exception as e:
        assert e.message[50:] == "Not all protectors agree with this address"

def test_changeOwner_2nd_require_part1(deploy):
    '''checking if the candidate protectorWaitingToBeOwner has the required number of votes'''
    try:
        deploy.changeOwner(accounts[9], {'from': accounts[protectorNextOwner]})       
    except Exception as e:
        assert e.message[50:] == "Not all protectors agree with this address"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeOwner_2nd_require_part2(deploy, protector):
    '''checking if the candidate protectorWaitingToBeOwner has the required number of votes'''
    try:
        deploy.voteCandidate(accounts[9], {'from': accounts[protector]})
        deploy.changeOwner(accounts[9], {'from': accounts[protectorNextOwner]})       
    except Exception as e:
        assert e.message[50:] == "Not all protectors agree with this address"

@pytest.mark.parametrize("protector2",  [addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeOwner_2nd_require_part3_1(deploy, protector2):
    '''checking if the candidate protectorWaitingToBeOwner has the required number of votes'''
    try:
        deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector1]})
        deploy.voteCandidate(accounts[9], {'from': accounts[protector2]})
        deploy.changeOwner(accounts[9], {'from': accounts[protectorNextOwner]})       
    except Exception as e:
        assert e.message[50:] == "Not all protectors agree with this address"

@pytest.mark.parametrize("protector2",  [addressProtector2, addressProtector4, addressProtector5])
def test_changeowner_2nd_require_part3_2(deploy, protector2):
    '''checking if this function can be called after 3 or more protectors agree'''
    try:
        deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector3]})
        deploy.voteCandidate(accounts[9], {'from': accounts[protector2]})
        deploy.changeOwner(accounts[9], {'from': accounts[protectorNextOwner]})
    except Exception as e:
        assert e.message[50:] == "Not all protectors agree with this address"

@pytest.mark.parametrize("protector2",  [addressProtector2, addressProtector5])
def test_changeowner_2nd_require_part3_3(deploy, protector2):
    '''checking if this function can be called after 3 or more protectors agree'''
    try:
        deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector4]})
        deploy.voteCandidate(accounts[9], {'from': accounts[protector2]})
        deploy.changeOwner(accounts[9], {'from': accounts[protectorNextOwner]})
    except Exception as e:
        assert e.message[50:] == "Not all protectors agree with this address"

def test_changeowner_2nd_require_part3_4(deploy):
    '''checking if this function can be called after 3 or more protectors agree'''
    try:
        deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector5]})
        deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector2]})
        deploy.changeOwner(accounts[9], {'from': accounts[protectorNextOwner]})
    except Exception as e:
        assert e.message[50:] == "Not all protectors agree with this address"

@pytest.mark.parametrize("protector",  [addressProtector3, addressProtector4, addressProtector5])
def test_changeOwner_2nd_require_part4_1(deploy, protector):
    '''checking if the candidate protectorWaitingToBeOwner has the required number of votes'''
    try:
        deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector1]})
        deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector2]})
        deploy.voteCandidate(accounts[9], {'from': accounts[protector]})
        deploy.changeOwner(accounts[9], {'from': accounts[protectorNextOwner]})       
    except Exception as e:
        assert e.message[50:] == "Not all protectors agree with this address"

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2])
@pytest.mark.parametrize("protector2",  [addressProtector4, addressProtector5])
def test_changeOwner_2nd_require_part4_2(deploy, protector, protector2):
    '''checking if the candidate protectorWaitingToBeOwner has the required number of votes'''
    try:
        deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector3]})
        deploy.voteCandidate(accounts[9], {'from': accounts[protector]})
        deploy.voteCandidate(accounts[9], {'from': accounts[protector2]})
        deploy.changeOwner(accounts[9], {'from': accounts[protectorNextOwner]})       
    except Exception as e:
        assert e.message[50:] == "Not all protectors agree with this address"

def test_changeOwner_2nd_require_part4_3(deploy):
    '''checking if the candidate protectorWaitingToBeOwner has the required number of votes'''
    try:
        deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector3]})
        deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector5]})
        deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector4]})
        deploy.changeOwner(accounts[9], {'from': accounts[protectorNextOwner]})       
    except Exception as e:
        assert e.message[50:] == "Not all protectors agree with this address"
      
@pytest.mark.parametrize("protector", [[3, 4, 5, 6], [3, 4, 5, 7], [3, 4, 6, 5], [3, 4, 6, 7], [3, 4, 7, 5], [3, 4, 7, 6], [3, 5, 4, 6], [3, 5, 4, 7], [3, 5, 6, 4], [3, 5, 6, 7], [3, 5, 7, 4], [3, 5, 7, 6], [3, 6, 4, 5], [3, 6, 4, 7], [3, 6, 5, 4], [3, 6, 5, 7], [3, 6, 7, 4], [3, 6, 7, 5], [3, 7, 4, 5], [3, 7, 4, 6], [3, 7, 5, 4], [3, 7, 5, 6], [3, 7, 6, 4], [3, 7, 6, 5], [4, 3, 5, 6], [4, 3, 5, 7], [4, 3, 6, 5], [4, 3, 6, 7], [4, 3, 7, 5], [4, 3, 7, 6], [4, 5, 3, 6], [4, 5, 3, 7], [4, 5, 6, 3], [4, 5, 6, 7], [4, 5, 7, 3], [4, 5, 7, 6], [4, 6, 3, 5], [4, 6, 3, 7], [4, 6, 5, 3], [4, 6, 5, 7], [4, 6, 7, 3], [4, 6, 7, 5], [4, 7, 3, 5], [4, 7, 3, 6], [4, 7, 5, 3], [4, 7, 5, 6], [4, 7, 
6, 3], [4, 7, 6, 5], [5, 3, 4, 6], [5, 3, 4, 7], [5, 3, 6, 4], [5, 3, 6, 7], [5, 3, 7, 4], [5, 3, 7, 6], [5, 4, 3, 6], [5, 4, 3, 7], [5, 4, 6, 3], [5, 4, 6, 7], [5, 4, 7, 3], [5, 4, 7, 6], [5, 6, 3, 4], [5, 6, 3, 7], [5, 6, 4, 3], [5, 6, 4, 7], [5, 6, 7, 3], [5, 6, 7, 4], [5, 7, 3, 4], [5, 7, 3, 6], [5, 7, 4, 3], [5, 7, 4, 6], [5, 7, 6, 3], [5, 7, 6, 4], [6, 3, 4, 5], [6, 3, 4, 7], [6, 3, 5, 4], [6, 3, 5, 7], [6, 3, 7, 4], [6, 3, 7, 5], [6, 4, 3, 5], [6, 4, 3, 7], [6, 4, 5, 3], [6, 4, 5, 7], [6, 4, 7, 3], [6, 4, 7, 5], [6, 5, 3, 4], [6, 5, 3, 7], [6, 5, 4, 3], [6, 5, 4, 7], [6, 5, 7, 3], [6, 5, 7, 4], [6, 7, 3, 4], [6, 7, 3, 5], [6, 7, 4, 3], [6, 7, 4, 5], [6, 7, 5, 3], [6, 7, 5, 4], [7, 3, 4, 5], [7, 3, 4, 6], [7, 3, 5, 4], [7, 3, 5, 6], [7, 3, 6, 4], [7, 3, 6, 5], [7, 4, 3, 5], [7, 4, 3, 6], [7, 4, 5, 
3], [7, 4, 5, 6], [7, 4, 6, 3], [7, 4, 6, 5], [7, 5, 3, 4], [7, 5, 3, 6], [7, 5, 4, 3], [7, 5, 4, 6], [7, 5, 6, 3], [7, 5, 6, 4], [7, 6, 3, 4], [7, 6, 3, 5], [7, 6, 4, 3], [7, 6, 4, 5], [7, 6, 5, 3], [7, 6, 5, 4]])
def test_changeOwner_2nd_require_part5(deploy, protector):
    '''checking if the candidate protectorWaitingToBeOwner has the required number of votes'''
    try:
        deploy.voteCandidate(accounts[9], {'from': accounts[protector[0]]})
        deploy.voteCandidate(accounts[9], {'from': accounts[protector[1]]})
        deploy.voteCandidate(accounts[9], {'from': accounts[protector[2]]})
        deploy.voteCandidate(accounts[9], {'from': accounts[protector[3]]})
        deploy.changeOwner(accounts[9], {'from': accounts[protectorNextOwner]})       
    except Exception as e:
        assert e.message[50:] == "Not all protectors agree with this address"

def test_changeOwner_2nd_require_part6(deploy):
    '''checking if the owner changes'''
    deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector1]})
    deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector2]})
    deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector3]})
    deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector4]})
    deploy.voteCandidate(accounts[9], {'from': accounts[addressProtector5]})
    deploy.changeOwner(accounts[9], {'from': accounts[protectorNextOwner]})
    assert deploy.protectorWaitingToBeOwner() ==  accounts[9]   

def test_changeOwner_candidateVotes_to_0(deploy):
    '''Checking if the candidateVotes for smartContractOwner is modified'''
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector1]})
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector2]})
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector3]})
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector4]})
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector5]})
    deploy.changeOwner(accounts[8], {'from': accounts[protectorNextOwner]})
    assert deploy.candidatesVotes(accounts[protectorOwnerAddress]) ==  0  

@pytest.mark.parametrize("protector",  [addressProtector1, addressProtector2, addressProtector3, addressProtector4, addressProtector5])
def test_changeOwner_alreadyVoted_to_false(deploy, protector):
    '''Checking if the protectors alreadyVoted changes to false'''
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector1]})
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector2]})
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector3]})
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector4]})
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector5]})
    deploy.changeOwner(accounts[8], {'from': accounts[protectorNextOwner]})
    assert deploy.alreadyVoted(accounts[protector], accounts[protectorOwnerAddress]) ==  False  

def test_changeOwner_protectorOwner_changed(deploy):
    '''Checking if the protectorOwner is modified'''
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector1]})
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector2]})
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector3]})
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector4]})
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector5]})
    deploy.changeOwner(accounts[8], {'from': accounts[protectorNextOwner]})
    assert deploy.smartcontractOwner() ==  accounts[protectorNextOwner] 

def test_changeOwner_protectorWaitingToBeOwner_changed(deploy):
    '''Checking if the protectorWaitingToBeOwner is modified'''
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector1]})
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector2]})
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector3]})
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector4]})
    deploy.voteCandidate(accounts[8], {'from': accounts[addressProtector5]})
    deploy.changeOwner(accounts[8], {'from': accounts[protectorNextOwner]})
    assert deploy.protectorWaitingToBeOwner() == accounts[8]



    '''TESTING RETURNPROTECTORS'''



def test_returnProtectors_1(deploy):
    '''Checking if the returnProtectors returns address of protector 1'''
    function_called = deploy.returnProtectors()
    assert function_called.events[0][0]["_address"] == accounts[addressProtector1]

def test_returnProtectors_2(deploy):
    '''Checking if the returnProtectors returns address of protector 2'''
    function_called = deploy.returnProtectors()
    assert function_called.events[1][0]["_address"] == accounts[addressProtector2]

def test_returnProtectors_3(deploy):
    '''Checking if the returnProtectors returns address of protector 3'''
    function_called = deploy.returnProtectors()
    assert function_called.events[2][0]["_address"] == accounts[addressProtector3]

def test_returnProtectors_4(deploy):
    '''Checking if the returnProtectors returns address of protector 4'''
    function_called = deploy.returnProtectors()
    assert function_called.events[3][0]["_address"] == accounts[addressProtector4]

def test_returnProtectors_5(deploy):
    '''Checking if the returnProtectors returns address of protector 5'''
    function_called = deploy.returnProtectors()
    assert function_called.events[4][0]["_address"] == accounts[addressProtector5]



'''TESTING ADDTOWHITELIST'''



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
def test_removedFromWhitelist_onlyprotectorOwner(deploy, not_owner):
    '''checking if only the protectorOwner can access this function'''
    with brownie.reverts("You are not the owner"):
        deploy.removedFromWhitelist(accounts[8], {'from': accounts[not_owner]}) 

def test_removeFromWhitelist_whitelist(deploy):
    '''checking if the address is removed to the whitelist'''
    deploy.addToWhitelist(accounts[8], {'from': accounts[protectorOwnerAddress]})
    deploy.removedFromWhitelist(accounts[8], {'from': accounts[protectorOwnerAddress]})
    assert deploy.whitelist(accounts[8]) == False

def test_removeFromWhitelist_multipletimes(deploy):
    '''checking if the whitelist returns false when address removed multiple times'''
    deploy.removedFromWhitelist(accounts[8], {'from': accounts[protectorOwnerAddress]})
    deploy.removedFromWhitelist(accounts[8], {'from': accounts[protectorOwnerAddress]})
    assert deploy.whitelist(accounts[8]) == False