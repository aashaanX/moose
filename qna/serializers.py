from rest_framework import serializers


class AddQuestionSerializer(serializers.Serializer):
    """
    Serializer for validating input for adding a question
    """
    question_title = serializers.CharField(required=True)
    question_description = serializers.CharField(required=True)

