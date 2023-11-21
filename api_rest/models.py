from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo de email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário deve ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150, default="")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

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

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'password', 'sexo', 'regiao', 'pdc', 'raca']


class Resultado_ia(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    resultado = models.CharField(max_length=150)