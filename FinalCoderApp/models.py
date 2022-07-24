from configparser import MissingSectionHeaderError
from distutils.command.upload import upload
from django.db import models
from django.forms import CharField, EmailField, URLField
from django.contrib.auth.models import User
import datetime
from django.utils import timezone


# Create your models here.
class Avatar(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='avatar/', blank=True, null=True)
    
class Inicio(models.Model):
    bievenida = models.CharField(max_length=100)

class Socio(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=30)
    edad = models.IntegerField()
    deportes = models.CharField(max_length=200)
    email = models.EmailField()
    def __str__(self):
        return f"Nombre: {self.nombre} - Apellido: {self.apellido} - Edad: {self.edad} - Deportes: {self.deportes} - Email: {self.email}"
    
class Deporte(models.Model):
    deporte = models.CharField(max_length=30)
    profesor = models.CharField(max_length=70)
    horario = models.CharField(max_length=60, default="Sin horario")

class Profesor(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=30)
    deporte = models.CharField(max_length=30)
    email = models.EmailField()

class Administrador(models.Model):
    puesto = models.CharField(max_length=100)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=30)
    email = models.EmailField()

class Foro(models.Model):
    comentarios = models.CharField(max_length=300)

class Comentario(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    creado_en = models.DateTimeField(default=timezone.now)
