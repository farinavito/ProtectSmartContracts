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