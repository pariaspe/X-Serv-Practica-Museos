from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Museo(models.Model):
    n_id = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=64)
    direccion = models.CharField(max_length=64)
    descripcion = models.TextField(blank=True)
    accesibilidad = models.BooleanField()
    barrio = models.CharField(max_length=32)
    distrito = models.CharField(max_length=32)
    url = models.URLField()
    telefono = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    pagina = models.CharField(max_length=64, default='Pagina de usuario')
    usuario_museo = models.ManyToManyField(Museo, blank=True)

    def __str__(self):
        return self.usuario.username

# Visto en: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Usuario.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.usuario.save()

class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario)
    museo = models.ForeignKey(Museo)
    comentario = models.TextField()
    fecha = models.DateTimeField()

    def __str__(self):
        return self.nomre + " " + self.fecha
