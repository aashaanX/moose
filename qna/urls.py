from django.urls import path

from . import views

urlpatterns = [
    path('add_question/', views.AddQuestion.as_view()),
    path('retrive_question/', views.RetriveQuestion.as_view()),
    path('add_answer/', views.AddAnswer.as_view()),
    path('add_question_comment/', views.AddQuestionComment.as_view()),
    path('add_answer_comment/', views.AddAnswerComment.as_view()),
]