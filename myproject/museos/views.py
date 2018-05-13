from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import Museo, Usuario
from django.contrib.auth.models import User
from django.db import IntegrityError

from django.template.loader import get_template
from django.template import Context
from django.views.decorators.csrf import csrf_exempt

from xml.sax import make_parser
from urllib import request, error
from xml.sax.handler import ContentHandler
import museos.parser

def print_museos():
    museos = Museo.objects.all()
    lista = 'Lista de museos:<ol>'
    for museo in museos:
        lista += '<li><a href="museos/' + str(museo.n_id) + '">' + museo.nombre + '</a></li>'
    lista += '</ol>'
    return lista

def update_museos():
    MuseoParser = make_parser()
    MuseoHandler = museos.parser.CounterHandler()
    MuseoParser.setContentHandler(MuseoHandler)

    xmlFile = request.urlopen('https://datos.madrid.es/egob/catalogo/201132-0-museos.xml')
    MuseoParser.parse(xmlFile)

    for i in range(len(MuseoHandler.titles)):
        museo = Museo(n_id=MuseoHandler.ids[i], nombre=MuseoHandler.titles[i])
        try:
            museo.save()
        except IntegrityError:
            pass
            #Museo.objects.filter(nombre=MuseoHandler.titles[i]).update(link=BarrapuntoHandler.links[i])

    return print_museos()

def print_usuarios():
    usuarios = User.objects.all()
    lista = 'Lista de usuarios:<ul>'
    for usuario in usuarios:
        try:
            ñoño = Usuario.objects.get(usuario=usuario) # ñoño no es utilizado
            lista += '<li><a href="' + usuario.username + '">' + usuario.username + '</a></li>'
        except Usuario.DoesNotExist:
            pass
    lista += '</ul>'
    return lista

# Create your views here.
@csrf_exempt
def barra(request):
    setAccesible = False
    if request.method == 'POST':
        cookies = request.COOKIES
        try:
            accesible = cookies['accesible'] == 'True'
            accesible = not accesible
        except KeyError:
            accesible = True
        setAccesible = True

    museos = print_museos()
    #museos = update_museos()
    usuarios = print_usuarios()
    template = get_template('annotated.html')
    response = HttpResponse(template.render(Context({'title': 'Mis Museos',
                                                 'content': museos + usuarios})))
    if setAccesible:
        response.set_cookie('accesible', value=accesible)
    return response

#Nombre provisional
def museo_todos(request):
    return HttpResponse('Museos')

def museo_id(request, mid):
    try:
        museo = Museo.objects.get(n_id=mid)
        template = get_template('annotated.html')
        return HttpResponse(template.render(Context({'title': museo.nombre,
                                                     'content': 'Info. Por desarrolar...'})))

    except Museo.DoesNotExist:
        return HttpResponseNotFound('404 NOT FOUND')

def usuario(request, nombre):
    try:
        usuario = User.objects.get(username=nombre)
        usuario = Usuario.objects.get(usuario=usuario)
        template = get_template('annotated.html')
        return HttpResponse(template.render(Context({'title': usuario.pagina,
                                                    'content': 'Info. Por desarrolar...'})))
    except Usuario.DoesNotExist:
        return HttpResponseNotFound('404 NOT FOUND')


def usuario_xml(request, name):
    return HttpResponse('Xml de ' + name)

def about(request):
    return HttpResponse('About')
