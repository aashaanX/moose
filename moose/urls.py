"""moose URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls.conf import include
import rest_framework
from django.contrib import admin
from django.urls import path
# from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('moose_user.urls')),
    path('qna/',include('qna.urls')),
    # path('graphql/', GraphQLView.as_view(graphiql=False)),
    #path('graphiql/', include('django_graphiql.urls')),
]
