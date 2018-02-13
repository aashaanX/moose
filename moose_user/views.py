from django.http.response import JsonResponse
from django.shortcuts import render
from django.test.client import JSON_CONTENT_TYPE_RE
from moose_user.models import MooseUser
from moose_user.serializers import MooseUserRegisterSerializer
from rest_framework import status
from rest_framework.response import Response
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
        moose_uesr_data = MooseUserRegisterSerializer(data=request.data)
        if moose_uesr_data.is_valid():
            user = MooseUser()
            user.set_password(moose_uesr_data.validated_data['password'])
            user.user_email= moose_uesr_data.validated_data['user_email']
            user.full_name = moose_uesr_data.validated_data['full_name']
            try:
                user.save()
                print(user)
                return Response(data={"SUCCESS": True, "Message":"User Created"},
                                status=status.HTTP_201_CREATED)
            except Exception:
                return Response(data={"SUCCESS": False, "ERORR": "Data is valid but user cannot be created"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data={"SUCCESS": False, "ERORR": "user data is invalid"},
                            status=status.HTTP_400_BAD_REQUEST)
