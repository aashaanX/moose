from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterMooseUser.as_view()),
    path('login/', views.LoginMooseUser.as_view()),
    path('logout/', views.LogoutMooseUser.as_view())
]