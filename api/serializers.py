# from .models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

UserModel = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["email", "password"]

    def validate_password(self, value):
        if len(value) < 8 or value.upper() == value or value.lower() == value:
            raise serializers.ValidationError(
                "The passowrd must be at least 8 characters long and contains both upper and lower case letters."
            )
        return value

    def create(self, validated_data):
        user = UserModel.objects.create(email=validated_data["email"],)
        # We need to use set_password to hash the password, otherwise, BasicAuthentication won't work.
        user.set_password(validated_data["password"])
        user.save()
        # token = Token.objects.create(user=user)
        token = Token.objects.get(user=user)
        user.api_key = token.key
        return user

    def to_representation(self, instance):
        return {"api_key": instance.api_key, "current": instance.value}
