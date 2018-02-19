from qna.models import Answer, Comment, Question
from rest_framework import serializers


class AddQuestionSerializer(serializers.Serializer):
    """
    Serializer for validating input for adding a question
    """
    question_title = serializers.CharField(required=True)
    question_description = serializers.CharField(required=True)

class AddAnswerSerializer(serializers.Serializer):
    """
    Serializer for validating input for adding answer
    """
    question_slug = serializers.CharField(required=True)
    answer_description = serializers.CharField(required=True)


class AddCommentQuestionSerializer(serializers.Serializer):
    """
    Serializer for Validating input for adding comment for a Question
    """
    question_slug = serializers.CharField(required=True)
    comment_description = serializers.CharField(required=True)


class RetriveQuestionSerializer(serializers.Serializer):
    """
    Serializer for validating question data for retrving question
    """
    question_slug = serializers.CharField(required=True)



class RetriveCommentOutputSerializer(serializers.ModelSerializer):

    moose_user_name = serializers.SerializerMethodField()

    def get_moose_user_name(self, obj):
        try:
            return obj.moose_user.full_name
        except:
            print("Error while serializing moose user full name")
            return ""

    class Meta:
        model = Comment
        fields = ('comment_slug', 'comment_description', 'moose_user_name')


class RetriveAnswerOutputSerializer(serializers.ModelSerializer):

    comments = RetriveCommentOutputSerializer(many=True)

    moose_user_name = serializers.SerializerMethodField()

    def get_moose_user_name(self, obj):
        try:
            return obj.moose_user.full_name
        except:
            print("Error while serializing moose user full name")
            return ""

    class Meta:
        model = Answer
        fields = ('answer_slug', 'answer_description', 'votes', 'moose_user_name', 'comments')



class RetriveQuestionOutputSerializer(serializers.ModelSerializer):
    comments = RetriveCommentOutputSerializer(many=True)
    answers = RetriveAnswerOutputSerializer(read_only=True, many=True)

    moose_user_name = serializers.SerializerMethodField()

    # answer_list = serializers.SerializerMethodField()


    # def get_answer_list(self,obj):
    #     answers = RetriveAnswerOutputSerializer(data=obj.answers, many=True)
    #     return answers.data

    def get_moose_user_name(self, obj):
        try:
            return obj.moose_user.full_name
        except:
            print("Error while serializing moose user full name")
            return ""

    class Meta:
        model = Question
        fields = ('question_slug', 'question_title', 'question_description', 'moose_user_name', 'question_status', 'comments', 'answers')


