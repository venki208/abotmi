from rest_framework import serializers
from datacenter.models import  AdvisorPublishedVideo

class AdvisorPublishedVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdvisorPublishedVideo
        

