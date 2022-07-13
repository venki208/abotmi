import os

from django.db import models
from datacenter.models import UserProfile

class BlockchainContracts(models.Model):
    '''
    Blockchain Contracts Maintanance
    ------------------------------
    FIELDS          : DESCRIPTION
    ------------------------------
    name            : Contract Name
    source_code     : solidity language contract code
    binary_format   : source code converted into binary format to compile
    contract_transaction_id : Hash value of the compiling binary format
    contract_address :  address of the contract using hash value
    '''
    name = models.CharField(max_length=20, blank=True)
    source_code = models.TextField(blank=True)
    binary_format = models.TextField(blank=True)
    contract_transaction_id = models.CharField(max_length=100, blank=True)
    contract_address = models.CharField(max_length=50, blank=True)
    created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now = True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True

class BlockchainAccounts(models.Model):
    '''
    Blockchain Accounts Maintanance
    ------------------------------
    FIELDS          : DESCRIPTION
    ------------------------------
    user_profile	    : user profile id one and one field
    accounts 	        : blockchain user account
    accounts_password   : blockcahing user account password
    accounts_creation_transaction_id : hash value of the set user detail transaction 
    is_account_created 	: blockchain user account creation is done with out failure (true / false)
    contract_address 	: foreignkey of the BlockchainContracts
    '''
    user_profile = models.OneToOneField(UserProfile)
    accounts = models.CharField(max_length=50, blank=True, null=True)
    accounts_password = models.CharField(max_length=50, blank=True, null=True)
    accounts_creation_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    is_account_created = models.BooleanField(default=0)
    contract_address = models.ForeignKey(BlockchainContracts)
    created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now = True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True