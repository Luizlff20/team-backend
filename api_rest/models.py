from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class Usuario(models.Model):

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length= 150, default="")
    email = models.EmailField(default="")
    senha = models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.senha = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.senha)
    
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)

    RACA_CHOICES = (
        ('B', 'Branca'),
        ('P', 'Preta'),
        ('A', 'Amarela'),
        ('PA', 'Parda'),
        ('I', 'Indígena'),
    )
    raca = models.CharField(max_length=2, choices=RACA_CHOICES)

    PDC_CHOICES = (
        ('S', 'Sim'),
        ('N', 'Não'),
    )
    pdc = models.CharField(max_length=1, choices=PDC_CHOICES)

    REGIAO_CHOICES = (
        ('N', 'Norte'),
        ('NE', 'Nordeste'),
        ('S', 'Sul'),
        ('SE', 'Suldeste'),
        ('CO', 'Centro-Oeste'),
    )
    regiao = models.CharField(max_length=2, choices=REGIAO_CHOICES)

class Resultado_ia(models.Model):
    id = models.AutoField(primary_key=True)
    usuario_id = models.IntegerField(default=0)
    resultado = models.CharField(max_length=150)
