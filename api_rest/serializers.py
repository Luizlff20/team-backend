from rest_framework import serializers
from .models import Usuario
from .models import Resultado_ia

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'username', 'sexo', 'raca', 'pdc', 'regiao']

class UsuarioSerializerRegister(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nome', 'username', 'password', 'sexo', 'raca', 'pdc', 'regiao']
        

class Resultado_iaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultado_ia
        fields = ['resultado']