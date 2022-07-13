from rest_framework import serializers
from rest_framework_mongoengine import serializers as document_serializers

from datacenter.models import Notification, NotificationTemplate, UserProfile

from common.notification.views import NotificationFunctions


class NotificationListSerializer(document_serializers.DocumentSerializer):

    def get_message(self, obj):
        data = NotificationFunctions.get_message_values(
            nf_obj=obj,
            notification_type=obj.template_id.template_type,
            user_profile=self.context.get('user_profile', None),
        )
        return {
            'message': obj.get_template(data['msg_data']),
            'profile_url': data['profile_url'],
            'profile_pic': data['profile_pic'],
            'action_url': data.get('action_url', ''),
            'action': data.get('action', False),
            'nf_type': obj.template_id.template_type
        }

    message = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = (
            'id',
            'read_status',
            'message',
            'created_date'
        )
