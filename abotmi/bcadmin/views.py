# Django Modules
from django.shortcuts import render
# Database Models
from datacenter.models import BlockchainAccounts, BlockchainContracts
# Local Imports
from login.decorators import allow_blockchain_admin

@allow_blockchain_admin
def index(request):
    """
    Steps: Display 
    """
    if request.method == 'GET':
        return render(request, 'blockchain/bc_home_view.html', locals())

@allow_blockchain_admin
def get_all_accounts(request):
    """
    Get all Blockchain accounts
    """
    if request.method == 'GET':
        user_accounts = BlockchainAccounts.objects.all()
        return render(request, 'blockchain/list_bc_accounts.html', locals())

@allow_blockchain_admin
def get_all_contracts(request):
    """
    Get all Blockchain Contracts
    """
    if request.method == 'GET':
        list_contract = BlockchainContracts.objects.all()
        return render(request, 'blockchain/list_bc_contract.html', locals())
        