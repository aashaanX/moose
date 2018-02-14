from django.db import models
from randomslugfield.fields import RandomSlugField

from moose_user.models import MooseUser


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_slug = RandomSlugField(length=9)
    moose_user = models.ForeignKey(MooseUser, on_delete=models.CASCADE)
    comment_description = models.TextField()

    def __str__(self):
        return self.comment_slug


class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    answer_slug = RandomSlugField(length=9)
    moose_user = models.ForeignKey(MooseUser, on_delete=models.CASCADE)
    answer_description = models.TextField()
    comments = models.ManyToManyField(Comment)
    votes = models.IntegerField(default=0, null=False)

    def __str__(self):
        return self.answer_slug


class Question(models.Model):
    STATUS = (
        ('open', 'open'),
        ('closed', 'closed'),
        ('wrong', 'wrong')
    )

    question_id = models.AutoField(primary_key=True)
    question_slug = RandomSlugField(length=9)
    moose_user = models.ForeignKey(MooseUser, on_delete=models.CASCADE)
    question_title = models.CharField(max_length=500)
    question_description = models.TextField(null=False)
    question_status = models.CharField(max_length=20, choices=STATUS, default='open')
    comments = models.ManyToManyField(Comment)
    answers = models.ManyToManyField(Answer)

    def __str__(self):
        return self.question_title + "|" + self.moose_user.full_name

    def get_answers(self):
        answers_set = self.answers.order_by('votes')
        return answers_set.values('moose_user__full_name', 'answer_description', 'votes')

    def get_comments(self):
        return self.comments.values('comment_description', 'moose_user__full_name')
