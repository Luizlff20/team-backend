from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Usuario 
from .models import Resultado_ia
from .serializers import UsuarioSerializer, UsuarioSerializerRegister

import json
# Create your views here.

@api_view(['GET'])
def get_users(request):
    if request.method == 'GET':
        users = Usuario.objects.all()
        serializer = UsuarioSerializer(users, many=True)
        formatted_response = {
            'success': True,
            'message': 'Lista de usuários recuperada com sucesso.',
            'data': serializer.data
        }
        return Response(formatted_response, status=status.HTTP_200_OK)
    return Response({'error': 'Requisição inválida'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_by_id(request, id):
    try: 
        user = Usuario.objects.get(pk=id)
    except:
        formatted_response = {
            'success': False,
            'message': 'Usuário não localizado.'
        }
        return Response(formatted_response, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UsuarioSerializer(user)
        formatted_response = {
            'success': True,
            'message': 'Usuário recuperado com sucesso.',
            'data': serializer.data
        }
        return Response(formatted_response, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def post_create_user(request):
    if request.method == 'POST':
        new_user = request.data
        serializer = UsuarioSerializerRegister(data=new_user)

        if serializer.is_valid():
            serializer.save()
            formatted_response = {
            'success': True,
            'message': 'Usuário criado com sucesso.',
            'data': serializer.data
        }
            return Response(formatted_response, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def put_edit_user(request, id):
    try:
        update_user = Usuario.objects.get(pk=id)
    except Usuario.DoesNotExist:
        formatted_response = {
            'success': False,
            'message': 'Usuário não localizado.'
        }
        return Response(formatted_response, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UsuarioSerializerRegister(update_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            formatted_response = {
            'success': True,
            'message': 'Usuário editado com sucesso.',
            'data': serializer.data
        }
            return Response(formatted_response, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_user(request, id):
    try:
        if request.method == 'DELETE':
            user_exists = Usuario.objects.filter(id=id).exists()
            if user_exists:
                Usuario.objects.filter(id=id).delete()
                return JsonResponse({'success': True, 'message': 'Usuário deletado com sucesso.'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'success': False, 'message': 'Usuário não localizado.'}, status=status.HTTP_404_NOT_FOUND)
    
    except:
        return JsonResponse({'success': False, 'message': 'Erro interno no servidor:'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
