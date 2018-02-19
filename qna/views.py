import logging

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from qna.models import Question, Answer, Comment
from qna.serializers import AddQuestionSerializer, RetriveQuestionSerializer, RetriveQuestionOutputSerializer, \
    AddAnswerSerializer, AddCommentQuestionSerializer, AddCommentAnswerSerializer

logger = logging.getLogger(__name__)

class AddQuestion(APIView):
    def post(self, request, format=None):
        try:
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
                    return Response(data={"SUCCESS": False, "msg": "Couldn't save question"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response(data={"SUCCESS": True, "msg": "Question Added"},
                                status=status.HTTP_200_OK)
            else:
                return Response(data={"SUCCESS": False, "msg": "Request params missing or wrong"},
                                status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(data={"SUCCESS": False, "msg": "Something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AddAnswer(APIView):

    def post(self, request, format=None):
        try:
            answer_data = AddAnswerSerializer(data=request.data)
            if answer_data.is_valid():
               answer=  Answer();
               try:
                   question = Question.objects.get(question_slug = answer_data.validated_data['question_slug'])
               except ObjectDoesNotExist:
                   return Response(data={"SUCCESS": False, "msg": "question doesn't exists"})
               try:
                   moose_user = request.user
               except:
                   return Response(data={"SUCCESS": False, "msg": "User Doesn't exists"})
               try:
                   answer.answer_description = answer_data.validated_data['answer_description']
                   answer.moose_user = moose_user
                   answer.save()
                   question.answers.add(answer)
                   question.save()
                   return Response(data={"SUCCESS":True, "msg": "Answer saved successfully"})
               except:
                   return Response(data={"SUCCESS": False, "msg": "Saving data failed"})
            else:
                return Response(data={"SUCCESS": False, "msg":"Request params missing or wrong"})
        except:
            return Response(data={"SUCCESS": False, "msg":"Something went wrong"})



class AddQuestionComment(APIView):

    def post(self, request, format=None):
        try:
            comment_data = AddCommentQuestionSerializer(data=request.data)
            if comment_data.is_valid():
                try:
                    question = Question.objects.get(question_slug=comment_data.validated_data['question_slug'])
                except ObjectDoesNotExist:
                    return Response(data={"SUCCESS": False, "msg": "question doesn't exists"})
                try:
                    moose_user = request.user
                except:
                    return Response(data={"SUCCESS": False, "msg": "User Doesn't exists"})
                try:
                    comment = Comment()
                    comment.comment_description = comment_data.validated_data['comment_description']
                    comment.moose_user = moose_user
                    comment.save()
                    question.comments.add(comment)
                    question.save()
                    return Response(data={"SUCCESS":True, "msg":"Comment saved successfully"})
                except:
                    return Response(data={"SUCCESS":False, "msg":"Saving data failed"})
            else:
                return Response(data={"SUCCESS":False, "msg":"Request param missing or wrong"})
        except:
            return Response(data={"SUCCESS":False, "msg": "Something went wrong"})


class AddAnswerComment(APIView):

    def post(self, request, format=None):
        try:
            comment_data = AddCommentAnswerSerializer(data=request.data)
            if comment_data.is_valid():
                try:
                    answer = Answer.objects.get(answer_slug=comment_data.validated_data['answer_slug'])
                except ObjectDoesNotExist:
                    return Response(data={"SUCCESS": False, "msg": "answer doesn't exists"})
                try:
                    moose_user = request.user
                except:
                    return Response(data={"SUCCESS": False, "msg": "User Doesn't exists"})
                try:
                    comment = Comment()
                    comment.comment_description = comment_data.validated_data['comment_description']
                    comment.moose_user = moose_user
                    comment.save()
                    answer.comments.add(comment)
                    answer.save()
                    return Response(data={"SUCCESS":True, "msg":"Comment saved successfully"})
                except:
                    return Response(data={"SUCCESS":False, "msg":"Saving data failed"})
            else:
                return Response(data={"SUCCESS":False, "msg":"Request param missing or wrong"})
        except:
            return Response(data={"SUCCESS":False, "msg": "Something went wrong"})




class RetriveQuestion(APIView):
    def post(self, request, format=None):
        try:
            request_data = RetriveQuestionSerializer(data=request.data)
            if request_data.is_valid():
                question_slug = request_data.validated_data["question_slug"]
                qusetion_data = Question.objects.get(question_slug=question_slug)
                question = RetriveQuestionOutputSerializer(qusetion_data)
                print("ggrggrg")
                print(question)
                return Response(data={'SUCCESS': True, 'question': question.data}, status=status.HTTP_200_OK)
            else:
                return Response(data={"SUCCESS": False, "msg": "request params missing or wrong"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception while retriving question | {}".format(e))
            return Response(data={"SUCCESS": False, "msg":"Something went Wrong"})



class VoteAnswer(APIView):

    def post(self, request, format=None):
        pass
