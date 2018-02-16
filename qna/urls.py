from django.urls import path

from . import views

urlpatterns = [
    path('add_question/', views.AddQuestion.as_view()),
    path('retrive_question/', views.RetriveQuestion.as_view()),
]