from rest_framework import serializers
from .models import Usuario
from .models import Resultado_ia

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'sexo', 'raca', 'pdc', 'regiao', 'is_active', 'is_staff']

class UsuarioSerializerRegister(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'password', 'sexo', 'raca', 'pdc', 'regiao', 'is_active', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Usuario.objects.create_user(password=password, **validated_data)
        return user
        

class Resultado_iaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultado_ia
        fields = ['resultado']