from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializers import (
    UserRegisterSerializer,
    CustomTokenObtainPairSerializer,
    UserRoleSerializer,
)



class UserRegisterView(CreateAPIView):
    """
    API endpoint for user registration.

    Expects a data : username, password, role 

    Returns : A JSON response with the created user 

    """

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Handles POST request and Checks for a valid "role" field in the request data.
        If the role is invalid, returns a 400 Bad Request error.
        Otherwise, calls the superclass's create method for further processing.

        """

        role = request.data.get("role", None)
        # validate role
        if role not in ("Candidate", "Employer"):
            return Response({"error": "Invalid role"}, status=HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRoleView(APIView):
    """
    API endpoint to retrieve a user's role information.

    Requires authentication (IsAuthenticated permission class).

    Returns : A JSON response

    """

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Handles GET requests to retrieve the authenticated user's role information.

        """

        user = request.user
        # validating user role serialization
        serializer = UserRoleSerializer(user)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
