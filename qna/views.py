import logging

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from qna.models import Question, Answer, Comment
from qna.serializers import AddQuestionSerializer, RetriveQuestionSerializer, RetriveQuestionOutputSerializer, \
    AddAnswerSerializer, AddCommentQuestionSerializer, AddCommentAnswerSerializer, VoteAnswerSerializer

logger = logging.getLogger(__name__)


class AddQuestion(APIView):
    "Class to add question"
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        """
        post Method to add question with moose user
        Parameters
        ----------
            request : json
                request from user
            format : string
                format of the request

        """
        try:
            logger.debug("Add Question request : {}".format(request.data))
            question_data = AddQuestionSerializer(data=request.data)
            if question_data.is_valid():
                logger.debug("question data is valid")
                question_title = question_data.validated_data["question_title"]
                question_description = question_data.validated_data["question_description"]
                question = Question()
                try:
                    question.moose_user = request.user
                except Exception as error:
                    logger.error("moose user cannot be set | {}".format(error))
                    return Response(data={"SUCCESS": False, "msg": "User not available"},
                                    status=status.HTTP_401_UNAUTHORIZED)
                question.question_title = question_title
                question.question_description = question_description
                try:
                    question.save()
                    logger.debug("Question saved")
                except Exception as error:
                    logger.error("Coundn't save question | {}".format(error))
                    return Response(data={"SUCCESS": False, "msg": "Couldn't save question"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response(data={"SUCCESS": True, "msg": "Question Added"},
                                status=status.HTTP_200_OK)
            else:
                logger.error("Validation of request data failed")
                return Response(data={"SUCCESS": False, "msg": "Request params missing or wrong"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            logger.error("Failed due to {}".format(error))
            return Response(data={"SUCCESS": False, "msg": "Something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddAnswer(APIView):
    """
    Class to add Answer
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        """
        post Method to add answer to a question
        Parameters
        ----------
            request : json
                request from user
            format : string
                format of the request

        """
        try:
            logger.debug("request for add answer : {}".format(request.data))
            answer_data = AddAnswerSerializer(data=request.data)
            if answer_data.is_valid():
                logger.debug("Answer data is validated")
                answer = Answer();
                try:
                    question = Question.objects.get(question_slug=answer_data.validated_data['question_slug'])
                    logger.debug("question : {}".format(question))
                except ObjectDoesNotExist:
                    logger.error("Question object not found")
                    return Response(data={"SUCCESS": False, "msg": "question doesn't exists"})
                try:
                    moose_user = request.user
                    logger.debug("moose user for adding answer : {}".format(moose_user))
                except:
                    logger.error("Moose user not found")
                    return Response(data={"SUCCESS": False, "msg": "User Doesn't exists"})
                try:
                    answer.answer_description = answer_data.validated_data['answer_description']
                    answer.moose_user = moose_user
                    answer.save()
                    logger.debug("Answer saved")
                    question.answers.add(answer)
                    question.save()
                    logger.debug("Question saved")
                    return Response(data={"SUCCESS": True, "msg": "Answer saved successfully"})
                except Exception as error:
                    logger.error("Error While trying to save answer | {}".format(error))
                    return Response(data={"SUCCESS": False, "msg": "Saving data failed"})
            else:
                logger.error("Data not validated")
                return Response(data={"SUCCESS": False, "msg": "Request params missing or wrong"})
        except Exception as error:
            logger.error("Unknown error | {}".format(error))
            return Response(data={"SUCCESS": False, "msg": "Something went wrong"})


class AddQuestionComment(APIView):
    """
    Class to add comment to a question
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        """
        post Method to add a comment to a question with moose user
        Parameters
        ----------
            request : json
                request from user
            format : string
                format of the request

        """
        logger.debug("Request for adding question comment : {}".format(request.data))
        try:
            comment_data = AddCommentQuestionSerializer(data=request.data)
            if comment_data.is_valid():
                logger.debug("comment data is validated")
                try:
                    question = Question.objects.get(question_slug=comment_data.validated_data['question_slug'])
                except ObjectDoesNotExist:
                    logger.error("Question object not found")
                    return Response(data={"SUCCESS": False, "msg": "question doesn't exists"})
                try:
                    moose_user = request.user
                except:
                    logger.error("Moose user not found")
                    return Response(data={"SUCCESS": False, "msg": "User Doesn't exists"})
                try:
                    comment = Comment()
                    comment.comment_description = comment_data.validated_data['comment_description']
                    comment.moose_user = moose_user
                    comment.save()
                    logger.debug("Comment Saved")
                    question.comments.add(comment)
                    question.save()
                    logger.debug("Question Saved")
                    return Response(data={"SUCCESS": True, "msg": "Comment saved successfully"})
                except Exception as error:
                    logger.error("Couldn't save comment | {}".format(error))
                    return Response(data={"SUCCESS": False, "msg": "Saving data failed"})
            else:
                logger.error("Data not validated")
                return Response(data={"SUCCESS": False, "msg": "Request param missing or wrong"})
        except Exception as error:
            logger.error("Unknow error : {}".format(error))
            return Response(data={"SUCCESS": False, "msg": "Something went wrong"})


class AddAnswerComment(APIView):
    """
    Class to add comment to an answer
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        """
        post Method to add comment to an answer with moose user
        Parameters
        ----------
            request : json
                request from user
            format : string
                format of the request

        """
        try:
            logger.debug("Request data for adding answer comment | {}".format(request.data))
            comment_data = AddCommentAnswerSerializer(data=request.data)
            if comment_data.is_valid():
                logger.debug("Comment data is valid")
                try:
                    answer = Answer.objects.get(answer_slug=comment_data.validated_data['answer_slug'])
                except ObjectDoesNotExist:
                    logger.error("Couldn't find the answer")
                    return Response(data={"SUCCESS": False, "msg": "answer doesn't exists"})
                try:
                    moose_user = request.user
                except:
                    logger.error("Couldn't find the moose user")
                    return Response(data={"SUCCESS": False, "msg": "User Doesn't exists"})
                try:
                    comment = Comment()
                    comment.comment_description = comment_data.validated_data['comment_description']
                    comment.moose_user = moose_user
                    comment.save()
                    logger.debug("comment saved")
                    answer.comments.add(comment)
                    answer.save()
                    logger.debug("answer saved")
                    return Response(data={"SUCCESS": True, "msg": "Comment saved successfully"})
                except Exception as error:
                    logger.error("Couldn't save comments for the answer | {}".format(error))
                    return Response(data={"SUCCESS": False, "msg": "Saving data failed"})
            else:
                logger.error("data not validated")
                return Response(data={"SUCCESS": False, "msg": "Request param missing or wrong"})
        except Exception as error:
            logger.error("Unkown error | {}".format(error))
            return Response(data={"SUCCESS": False, "msg": "Something went wrong"})


class RetriveQuestion(APIView):
    """
    Class to retrive Question details
    """

    def post(self, request, format=None):
        """
        post Method to retrive Question details based on question_slug provided

        Parameters
        ----------
            request : json
                request from user
            format : string
                format of the request
        """
        try:
            logger.debug("Request data to retrive Question | {}".format(request.data))
            request_data = RetriveQuestionSerializer(data=request.data)
            if request_data.is_valid():
                logger.debug("request data is valid")
                question_slug = request_data.validated_data["question_slug"]
                qusetion_data = Question.objects.get(question_slug=question_slug)
                question = RetriveQuestionOutputSerializer(qusetion_data)
                return Response(data={'SUCCESS': True, 'question': question.data}, status=status.HTTP_200_OK)
            else:
                logger.error("Requested data is not valid")
                return Response(data={"SUCCESS": False, "msg": "request params missing or wrong"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Exception while retriving question | {}".format(e))
            return Response(data={"SUCCESS": False, "msg": "Something went Wrong"})


class VoteAnswer(APIView):
    """class to vote for the answers"""
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        """
        post Method to vote for an answer
        Parameters
        ----------
            request : json
                request from user
            format : string
                format of the request

        """
        try:
            requested_data = VoteAnswerSerializer(data=request.data)
            if requested_data.is_valid():
                logger.debug("request data is valid")
                try:
                    answer = Answer.objects.get(answer_slug=requested_data['answer_slug'])
                except Exception as error:
                    logger.error("Couldn't get answer object | {}".format(error))
                    return Response(data={"SUCCESS": False, "msg": "answer doesn't exists"})
                if requested_data['vote']:
                    moose_user = request.user
                    answer.votes.add(moose_user)
                    answer.save()
                    logger.debug("answer object saved")
                    return Response(data={"SUCCESS": True, "msg": "answer voted"})
            else:
                return Response(data={"SUCCESS": False, "msg": "request params missing or wrong"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            logger.error("Exception while Voting | {}".format(error))
            return Response(data={"SUCCESS": False, "msg": "Something went Wrong"})
