from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView 
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import permissions
from .serializers import UserCreateSerializer 
from .authentication import BearerTokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.models import Token

UserModel = get_user_model()

class SignUpView(CreateAPIView):
    model = UserModel 
    permissions_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserCreateSerializer

@api_view(['GET'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_next(request, format=None):
    user = request.user
    user.value += 1
    user.save()
    return Response({"current": user.value})

@api_view(['GET'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_current(request, format=None):
    user = request.user
    return Response({"current": user.value})

@api_view(['PUT'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def reset(request, format=None):
    user = request.user
    user.value = request.data['current']
    user.save()
    return Response({"current": user.value})

@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([permissions.IsAuthenticated])
def api_key(request, format=None):
    token = Token.objects.get(user=request.user)
    if not token:
        token = Token.objects.create(user=request.user)
        token.save()
    return Response({"api_key": token.key})