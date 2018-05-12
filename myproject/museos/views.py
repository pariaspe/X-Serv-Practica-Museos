from django.shortcuts import render
from django.http import HttpResponse
from .models import Museo
from django.db import IntegrityError

from django.template.loader import get_template
from django.template import Context

from xml.sax import make_parser
from urllib import request, error
from xml.sax.handler import ContentHandler
import museos.parser

def print_museos():
    museos = Museo.objects.all()
    lista = 'Lista de museos:<ol>'
    for museo in museos:
        lista += '<li>' + museo.nombre + '</li>'
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

# Create your views here.
def barra(request):
    title = '<h1>Mis Museos</h1>'
    prueba = print_museos()
    #prueba = update_museos()
    template = get_template('annotated.html')
    return HttpResponse(template.render(Context({'title': title,
                                                 'content': prueba})))

#Nombre provisional
def museo_todos(request):
    return HttpResponse('Museos')

def museo_id(request, mid):
    return HttpResponse('Museo ' + mid)

def usuario(request, name):
    return HttpResponse('Usuario ' + name)

def usuario_xml(request, name):
    return HttpResponse('Xml de ' + name)

def about(request):
    return HttpResponse('About')
