from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Location
from .serializer import RegisterSerializer, LoginSerializer, SearchSerializer


class RegisterCreateAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        print('user', user)
        serializer = self.serializer_class(data=user)
        print('serializer', serializer)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'data': 'Successfully created'}, status=status.HTTP_201_CREATED)


class LoginCreateApi(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Successfully log in'}, status=status.HTTP_201_CREATED)





