from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField()
    contraseña = models.CharField()
    pagina = models.CharField()
    usuario_museo = models.ManyToManiField(Museo)
    
    def __str__(self):
        return self.nombre

class Museo(models.Model):
    nombre = models.CharField()

    def __str__(self):
        return self.nombre

class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario)
    museo = models.ForeignKey(Museo)
    comentario = models.TextField()
    fecha = models.DateTimeField()

    def __str__(self):
        return self.nomre + " " + self.fecha
