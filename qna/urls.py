from django.urls import path

from . import views

urlpatterns = [
    path('add_question/', views.AddQuestion.as_view())
]