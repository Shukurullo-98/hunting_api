from django.shortcuts import render
from rest_framework.response import Response

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from authentication.models import *
from authentication.serializer import UserCreateApiSerializer
from rest_framework.permissions import IsAuthenticated


class UserCreateApiView(CreateAPIView):
    model = User
    serializer_class = UserCreateApiSerializer




class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "User has no auth token."}, status=status.HTTP_400_BAD_REQUEST)