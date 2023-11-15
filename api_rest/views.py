from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Usuario 
from .models import Resultado_ia
from .serializers import UsuarioSerializer

import json
# Create your views here.

@api_view(['GET'])
def get_users(request):
    if request.method == 'GET':
        users = Usuario.objects.all()
        serializer = UsuarioSerializer(users, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_by_id(request, id):

    try: 
        user = Usuario.objects.get(pk=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UsuarioSerializer(user)
        return Response(serializer.data)
    

@api_view(['POST'])
def post_create_user(request):
    if request.method == 'POST':
        new_user = request.data
        serializer = UsuarioSerializer(data=new_user)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def put_edit_user(request, id):
    try:
        update_user = Usuario.objects.get(pk=id)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UsuarioSerializer(update_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_deleted_user(request, id):  
    try:
        if request.method == 'DELETE':  
            Usuario.objects.filter(id=id).delete()
            return Response(status=status.HTTP_200_OK)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)   
        
