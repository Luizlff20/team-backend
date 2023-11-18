from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

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
            if ('password' in request.data):
                password = make_password(request.data['password'])
                serializer.save(password=password)
            else:
                serializer.save()

            formatted_response = {
                'success': True,
                'message': 'Usuário criado com sucesso.',
                'data': serializer.data
            }
            return Response(formatted_response, status=status.HTTP_201_CREATED)
        formatted_response = {
            'success': False,
            'message': 'Usuário já cadastrado.'
        }
        return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)


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
@permission_classes([IsAuthenticated])
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


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties = {
                'username' : openapi.Schema(type=openapi.TYPE_STRING, description='email usuário'),
                'password' : openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description='senha usuário')
            }
        )

    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Campos não preenchidos'}, status=status.HTTP_400_BAD_REQUEST)

        user = Usuario.objects.get(username=username)
        if user is None:
            return Response({'error': 'Email inválido'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.check_password(password):
            return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True,
            'message': 'Usuário autenticado com sucesso.',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
        