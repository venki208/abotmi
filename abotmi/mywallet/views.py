"""
Description     : This is mywallet application views. This app helps to manage create wallet, earn wallet, pay wallet
Creation Date   : 13 DEC 2017
Functions       : createWallet, addWalletMoney, payWalletMoney, walletTransaction
Models          : mywallet.py (MyWallet, MyWalletTransaction)
"""
# python lib
import logging
# Database models
from datacenter.models import MyWallet, MywalletTransaction
# constants
from mywallet import constants

logger = logging.getLogger(__name__)

class Wallet:
    def createWallet(self, user):
        '''
        Descirption : To create Wallet
        Arguments : user(user_profile object)
        Return : MyWallet object
        '''
        exists, wallet_account = MyWallet.objects.get_or_create (
            user_profile = user,
            wallet_name = constants.WALLET_NAME
        )
        if exists:
            return exists
        else:
            return wallet_account


    def addWalletMoney(self, user, amount, txn):
        '''
        Descirption : To add wallet money in respective user wallet
        Arguments : user (user_profile object), amoutn (amount to add in wallet), txn(belongs to whcih transaction)
        Return : Nothing
        '''
        wallet_obj = self.createWallet(user)
        if wallet_obj:
            wallet_money = float(amount) * (float(1)/float(100) * constants.REFFERAL_PERCENTAGE)
            wallet_obj.total_wallet = wallet_money + wallet_obj.total_wallet
            wallet_obj.save()
            self.walletTransaaction(user, wallet_obj.wallet_name, txn, amount, None)


    def payWalletMoney(self, user, amount, txn):
        '''
        Descirption : To pay money through wallet money
        Arguments : user (user_profile object), amoutn (amount to add in wallet), txn(belongs to whcih transaction)
        Return : Nothing
        '''
        wallet_obj = self.createWallet(user)
        if wallet_obj:
            wallet_money = float(amount) * (float(1)/float(100) * constants.REFFERAL_PERCENTAGE)
            if wallet_obj.total_wallet > wallet_money:
                wallet_money = wallet_obj.total_wallet
            wallet_obj.total_wallet = wallet_obj.total_wallet - wallet_money
            wallet_obj.save()
            self.walletTransaaction(user, wallet_name, txn_obj, None, amount)


    def walletTransaaction(self, user, wallet_name, txn_obj, receivable, payable):
        '''
        Descirption : To manage the pay and earn wallet money transaction
        Arguments : user (user_profile object), wallet_name, txn(belongs to whcih transaction), receivable, payable 
        Return : Nothing
        '''
        wallet_txn = MywalletTransaction.objects.create(
            user_profile = user,
            wallet_name = wallet_name,
            source_transaction = txn_obj
        )
        if receivable:
            wallet_txn.credited_amount = receivable
        if payable:
            debited_amount = payable
        wallet_txn.save()