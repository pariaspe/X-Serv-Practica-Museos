from django.db import models

# Create your models here.
class Museo(models.Model):
    nombre = models.CharField(max_length=64)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    nombre = models.CharField(max_length=32)
    contraseña = models.CharField(max_length=32)
    pagina = models.CharField(max_length=64)
    usuario_museo = models.ManyToManyField(Museo)

    def __str__(self):
        return self.nombre

class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario)
    museo = models.ForeignKey(Museo)
    comentario = models.TextField()
    fecha = models.DateTimeField()

    def __str__(self):
        return self.nomre + " " + self.fecha
