from rest_framework import serializers
from surveys.models import Survey, SurveyResponse

class SurveySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=200)
    available_places = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)

    def create(self, validated_data):
        """
        Create and return a new `Survey` instance, given the validated data.
        """
        return Survey.objects.create(**validated_data)


class SurveyResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    survey_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)
    created_at = serializers.DateTimeField(required=False, read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `SurveyResponse` instance, given the validated data.
        """
        instance = SurveyResponse.objects.create(**validated_data)
        return instance
