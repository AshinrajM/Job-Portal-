import re
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from django.contrib.auth.password_validation import validate_password


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email", "password", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    # Custom password validation
    def validate_password(self, value):
        """
        Check that the password is at least 6 characters long,
        contains both alphabets and digits, and has no spaces.
        """
        if len(value) < 6:
            raise serializers.ValidationError(
                "Password must be at least 6 characters long."
            )

        if not re.search(r"[A-Za-z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one letter."
            )

        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                "Password must contain at least one digit."
            )

        if " " in value:
            raise serializers.ValidationError("Password should not contain spaces.")

        return value

    # Custom username validation
    def validate_username(self, value):
        """
        Validate the username

        """
        if " " in value:
            raise serializers.ValidationError("Username should not contain spaces.")

        if not re.match(r"^\w+$", value):
            raise serializers.ValidationError(
                "Username can only contain letters, digits, and underscores."
            )

        return value

    # Custom email validation (standard Django validation applies, but you can add extra)
    def validate_email(self, value):
        """
        Validate the email to standard email format.

        """
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
            raise serializers.ValidationError("Enter a valid email address.")

        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role=validated_data["role"],
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        return token


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "role"]
