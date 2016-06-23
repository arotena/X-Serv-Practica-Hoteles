from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Hoteles (models.Model):
    nombre = models.CharField(max_length = 200)
    web = models.URLField()
    email = models.CharField(max_length = 200,default="")
    phone = models.CharField(max_length = 200,default="")
    body = models.TextField(default="")
    address = models.CharField(max_length = 200)
    country = models.CharField(max_length = 200)
    categoria = models.TextField(default="")
    subcategoria = models.TextField(default="")
    nComentario = models.IntegerField()
class Imagenes (models.Model):
    src =  models.URLField();
    hotel = models.ForeignKey(Hoteles)
class Colecciones(models.Model):
    usuario = models.TextField(default="")
    alojamiento = models.CharField(max_length=32)
    date = models.DateField(auto_now=True)
class Comentarios(models.Model):
    usuario = models.TextField(default="")
    contenido = models.TextField(default="")
    hotel = models.CharField(max_length=32)
class Css(models.Model):
    usuario = models.TextField(default="")
    color = models.CharField(max_length=32)
    size = models.CharField(max_length=32)
    title = models.TextField(default="")
