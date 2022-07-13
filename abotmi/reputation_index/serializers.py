from rest_framework import serializers
from datacenter.models import ReputationIndexMetaData, AdvisorReputationIndex


class ReputationIndexMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReputationIndexMetaData
        exclude = ('id','user_profile', 'created_date', 'modified_date')

class AdvisorReputationIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvisorReputationIndex
        
