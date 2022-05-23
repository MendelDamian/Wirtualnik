from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieve and update user endpoint.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "date_joined",
            "email",
            "uuid",
        )
        read_only_fields = ("username", "date_joined", "uuid",)


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer for create user endpoint.
    """

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "date_joined",
            "uuid",
            "auth_token",
        )
        read_only_fields = ("auth_token", "date_joined", "uuid",)
        extra_kwargs = {
            "password": {"write_only": True},
            "uuid": {"read_only": True},
            "auth_token": {"read_only": True},
            "date_joined": {"read_only": True},
        }


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
