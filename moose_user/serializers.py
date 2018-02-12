from rest_framework import serializers


class MooseUserRegisterSerializer(serializers.Serializer):
    """
    Serializer for validating input for registering a patient
    """
    user_email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type':'password'})
    full_name = serializers.CharField(required=False)
    about_user = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    dob = serializers.DateTimeField(required=False)

