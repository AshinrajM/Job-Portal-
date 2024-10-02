from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UserRegisterView



urlpatterns = [
    path('api/register/',UserRegisterView.as_view(), name='register')

]