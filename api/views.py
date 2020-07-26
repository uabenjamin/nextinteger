from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveAPIView,
)
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import permissions
from .serializers import UserCreateSerializer
from .authentication import BearerTokenAuthentication
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.models import Token
from api.models import SocialAuthUser

UserModel = get_user_model()
headers = {
    "Access-Control-Allow-Origin": "*",
}


class SignUpView(CreateAPIView):
    model = UserModel
    permissions_classes = [permissions.AllowAny]
    serializer_class = UserCreateSerializer


@api_view(["GET"])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_next(request, format=None):
    user = request.user
    user.value += 1
    user.save()
    return Response({"current": user.value})


@api_view(["GET"])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_current(request, format=None):
    user = request.user
    return Response({"current": user.value})


@api_view(["PUT"])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def reset(request, format=None):
    user = request.user
    user.value = request.data["current"]
    user.save()
    return Response({"current": user.value})


@api_view(["PUT"])
@authentication_classes([BasicAuthentication])
@permission_classes([permissions.IsAuthenticated])
def api_key(request, format=None):
    token = Token.objects.get(user=request.user)
    if not token:
        token = Token.objects.create(user=request.user)
        token.save()
    return Response({"api_key": token.key}, headers=headers)


@api_view(["POST"])
@authentication_classes([BasicAuthentication, BearerTokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def signin(request, format=None):
    token = Token.objects.get(user=request.user)
    if not token:
        token = Token.objects.create(user=request.user)
        token.save()
    return Response({"api_key": token.key, "current": request.user.value})


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def social_signin(request, format=None):
    access_token = request.data["access_token"]
    email = request.data["email"]
    matching_users = SocialAuthUser.objects.filter(email=email)
    if len(matching_users):
        auth_user = matching_users[0]
        token = Token.objects.get(user=auth_user.user)
    else:
        user = UserModel.objects.create(email=email, password=access_token[:10])
        user.save()
        token = Token.objects.get(user=user)
        auth_user = SocialAuthUser.objects.create(
            email=email, provider=request.data["provider"], user=user
        )
        auth_user.save()
    return Response({"api_key": token.key, "current": auth_user.user.value})
