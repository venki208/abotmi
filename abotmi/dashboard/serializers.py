from datacenter.models import TrackReferrals,UserProfile,RevenueTransactions
from rest_framework import serializers
from django.db.models import Sum

class TrackReferralsSerializer(serializers.ModelSerializer):
    """
    serializers: Track Referrals Serializer
    """
    def get_userprofile(self, obj):
        userprofile=UserProfile.objects.filter(email=obj.email).first()
        if userprofile:
            user_profile = {
                'email':userprofile.email,
                'first_name' : userprofile.first_name,
                'is_register_advisor' : userprofile.advisor.is_register_advisor,
                'is_registered_advisor' : userprofile.advisor.is_registered_advisor,
                'is_stream_user': userprofile.advisor.is_wpb_user
            }
            return user_profile
        else:
            return ''
    def get_earnings_and_transaction(self, obj):
        userprofile=UserProfile.objects.filter(email=obj.email).first()
        if userprofile:
            earnings =0
            transaction_count=0
            revenue_transactions = RevenueTransactions.objects.filter(pay_to=userprofile,is_paid=True)
            if revenue_transactions:
                earnings = revenue_transactions.aggregate(Sum('revenue'))
                transaction_count = revenue_transactions.count()
            earnings_and_transaction = {
                'earnings':earnings,
                'transaction_count' : transaction_count
            }
            return earnings_and_transaction
        else:
            return ''
    userprofile = serializers.SerializerMethodField()
    earnings_and_transaction = serializers.SerializerMethodField()
    class Meta:
        model = TrackReferrals
        
        fields = (
            'userprofile',
            'earnings_and_transaction',
            'id',
            'name',
            'email',
            'phone',
            'location',
            'products_serviced',
            'registered_financial_advisor',
            'sebi_reg_no',
            'amfi_reg_no',
            'irda_reg_no',
            'crisil_verified_no',
            'know_duration',
            'believe_become_advisor',
            'referral_user_type',
            'created_date',
            'modified_date'
        )
