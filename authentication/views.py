from django.http import HttpResponse
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import User
from .serializers import UserRegisterSerializer,CustomTokenObtainPairSerializer,UserRoleSerializer

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self,request,*args,**kwargs):
        role = request.data.get('role',None)
        if role not in ['Candidate', 'Employer']:
            return Response({'error':'Invalid role'},status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRoleView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = UserRoleSerializer(user)
        return Response(serializer.data)