from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.shortcuts import render
from django.test.client import JSON_CONTENT_TYPE_RE
from moose_user.models import MooseUser
from moose_user.serializers import MooseUserRegisterSerializer, MooseUserLoginSerializer
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
            user.user_email = moose_uesr_data.validated_data['user_email']
            user.full_name = moose_uesr_data.validated_data['full_name']
            try:
                user.save()
                print(user)
                return Response(data={"SUCCESS": True, "Message": "User Created"},
                                status=status.HTTP_201_CREATED)
            except Exception:
                return Response(data={"SUCCESS": False, "ERORR": "Data is valid but user cannot be created"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data={"SUCCESS": False, "ERORR": "user data is invalid"},
                            status=status.HTTP_400_BAD_REQUEST)


class LoginMooseUser(APIView):
    def post(self, request, format=None):
        print(request.data)
        login_credentials = MooseUserLoginSerializer(data=request.data)
        if login_credentials.is_valid():
            user_email = login_credentials.validated_data["user_email"]
            password = login_credentials.validated_data["password"]
            try:
                moose_user = MooseUser.objects.get(user_email=user_email)
            except ObjectDoesNotExist as e:
                print("Error while trying to retrive moose user| {}".format(e))
                return Response(data={"SUCCESS": False, "msg": "Wrong username/ password"},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                moose_user.status = 'available'
                moose_user.save()
                user = authenticate(user_email=user_email, password=password)
            except Exception as e:
                moose_user.status = 'offline'
                moose_user.save()
                print("Error while trying to authenticate user | {}".format(e))
                return Response(data={"SUCCESS": False, "msg": "Wrong username/ password"},
                                status=status.HTTP_400_BAD_REQUEST)

            if user is not None:
                login(request, user)
            if moose_user.active:
                return Response(data={"SUCCESS": True, "msg": "User Authenticated successfully"},
                                status=status.HTTP_200_OK)
        else:
            return Response(data={"SUCCESS": False, "msg": "login credentials not validated"},
                            status=status.HTTP_400_BAD_REQUEST)


class LogoutMooseUser(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            user_name = str(request.user).split("|")[0].strip()
            try:
                moose_user = MooseUser.objects.get(user_email=user_name)
            except Exception as e:
                print("Cannot get moose user")
                return Response({"SUCCESS": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            moose_user.status = 'offline'
            moose_user.save()
            logout(request)
        return Response({"SUCCESS": True}, status=status.HTTP_200_OK)
