from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *



urlpatterns = [
    path('register/',UserRegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('role/', UserRoleView.as_view(), name='user_role'),

]

