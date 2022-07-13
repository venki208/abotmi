import json
from rest_framework import serializers
from .models import AdvisorData

class AdvisorCheckSerializer(serializers.ModelSerializer):

	def get_registrations(self, obj):
		if obj.registrations:
			return json.loads(obj.registrations)
		else:
			return ''
	registrations = serializers.SerializerMethodField()

	class Meta:
		model = AdvisorData