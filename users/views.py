from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


class CustomUserViewSet(GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED )
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
