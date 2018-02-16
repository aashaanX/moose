from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from qna.models import Question
from qna.serializers import AddQuestionSerializer


class AddQuestion(APIView):

    def post(self, request, format=None):
        question_data = AddQuestionSerializer(data=request.data)
        if question_data.is_valid():
            question_title = question_data.validated_data["question_title"]
            question_description = question_data.validated_data["question_description"]
            question = Question()
            try:
                question.moose_user = request.user
            except:
                return Response(data={"SUCCESS": False, "msg": "User not available"},
                                status=status.HTTP_401_UNAUTHORIZED)
            question.question_title = question_title
            question.question_description = question_description
            try:
                question.save()
            except:
                return Response(data={"SUCCESS": False, "msg": "UnKnown"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(data={"SUCCESS": True, "msg": "Question Added"},
                            status=status.HTTP_200_OK)
        else:
            return Response(data={"SUCCESS": False, "msg": "request params missing or wrong"},
                            status=status.HTTP_400_BAD_REQUEST)
