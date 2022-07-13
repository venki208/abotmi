from rest_framework import serializers
from datacenter.models import RevenueTransactions, UserProfile, RevenueType, \
    ClientPlatform, ClientDetails

class RevenueTransactionsSerializer(serializers.ModelSerializer):
    """
    serializers: Revenue Transactions Serializer
    """
    class Meta:
        model = RevenueTransactions

class RevenueTypeSerializer(serializers.ModelSerializer):
    """
    serializers: Revenue Type Serializer
    """
    class Meta:
        model = RevenueType

class PlatformSerializer(serializers.ModelSerializer):
    """
    serializers: Platform Serializer
    """
    class Meta:
        model = ClientPlatform

class ClientSerializer(serializers.ModelSerializer):
    """
    serializers: Platform Serializer
    """
    class Meta:
        model = ClientDetails