from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView

)
from .serializers import UserCreateSerializer,RetrieveUpdateDestroySerializer,ProfilePasswordUpdateSerializer,UserLoginSerializer

User = get_user_model()


class UserLogin(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ProfileCreateList(ListCreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()


class ProfileRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = RetrieveUpdateDestroySerializer
    queryset = User.objects.all()
    lookup_field = 'pk'


class ProfilePasswordUpdate(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfilePasswordUpdateSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'
