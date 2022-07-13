from rest_framework import serializers
from datacenter.models import UserProfile

class WebinarUserProfileData(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'first_name',
            'email'
        )
