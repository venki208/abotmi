from rest_framework import serializers
import pandas as pd


class BulkAdvisorDataSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        try:
            data_frame = pd.DataFrame.from_dict(data)
            return data_frame
        except ValueError as e:
            raise ValidationError({api_settings.NON_FIELD_ERRORS_KEY: [str(e)]})

    def to_representation(self, instance):
        instance = instance.rename(index=str)
        return instance.to_dict(orient='index')
