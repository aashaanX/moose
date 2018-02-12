from django.http.response import JsonResponse
from django.shortcuts import render
from django.test.client import JSON_CONTENT_TYPE_RE
from moose_user.serializers import MooseUserRegisterSerializer
from rest_framework.views import APIView


class RegisterMooseUser(APIView):
    """
    API to regster user
    """

    def post(self, request, format=None):
        """
        API to register a new Moose user; to register a admin user please contact the admin
        :param request: request from the external app
        :param format: format of the request
        :return: json with success is true if moose user registered succesfully else will be providing the Error message
        """

        print(request)
        moose_uesr_data = MooseUserRegisterSerializer(request.data)
        if moose_uesr_data.is_valid():
            pass
        else:
            return {}