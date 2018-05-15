from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import Museo, Usuario, Comentario
from django.contrib.auth.models import User
from django.db import IntegrityError

from django.template.loader import get_template
from django.template import Context
from django.views.decorators.csrf import csrf_exempt

from xml.sax import make_parser
from urllib import request, error
from xml.sax.handler import ContentHandler
import museos.parser
import datetime

def print_museos(distrito):
    if distrito == '':
        museos = Museo.objects.all()
    else:
        museos = Museo.objects.filter(distrito=distrito)
    lista = 'Lista de museos:<ol>'
    for museo in museos:
        lista += '<li><a href="museos/' + str(museo.n_id) + '">' + museo.nombre + '</a></li>'
    lista += '</ol>'
    return lista

def print_accesibles(distrito):
    if distrito == '':
        museos = Museo.objects.filter(accesibilidad=True)
    else:
        museos = Museo.objects.filter(accesibilidad=True).filter(distrito=distrito)
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

    for i in range(len(MuseoHandler.nombres)):
        accesibilidad = MuseoHandler.accesibilidad[i] == '1'
        telefono, email = MuseoHandler.contactos[i]
        museo = Museo(n_id=MuseoHandler.ids[i], nombre=MuseoHandler.nombres[i],
            direccion=MuseoHandler.direcciones[i], descripcion=MuseoHandler.descripciones[i], accesibilidad=accesibilidad,
            barrio=MuseoHandler.barrios[i], distrito=MuseoHandler.distritos[i], url=MuseoHandler.urls[i], telefono=telefono, email=email)
        try:
            museo.save()
        except IntegrityError:
            pass
            #Museo.objects.filter(nombre=MuseoHandler.titles[i]).update(link=BarrapuntoHandler.links[i]) # TODO

    return print_museos()

def print_usuarios():
    usuarios = User.objects.all()
    lista = 'Lista de usuarios:<ul>'
    for usuario in usuarios:
        try:
            ñoño = Usuario.objects.get(usuario=usuario) # TODO ñoño no es utilizado
            lista += '<li><a href="' + usuario.username + '">' + usuario.username + '</a></li>'
        except Usuario.DoesNotExist:
            pass
    lista += '</ul>'
    return lista

def select_box():
    distritos = Museo.objects.all().values_list('distrito', flat=True).distinct()
    select = '<select name="distrito">'
    select += '<option value="">------</option>'
    for distrito in distritos:
        select += '<option value="' + distrito + '">' + distrito + '</option>'
    select += '</select>'
    return select

def print_comentarios(mid):
    comentarios = Comentario.objects.filter(m_id=mid)
    info = '<b><u>Comentario:</u></b><br/>'
    for comentario in comentarios:
        info += comentario.username + ': ' + comentario.comentario + ' at ' + str(comentario.fecha) + '<br/>'

    return info

def print_museo_info(museo):
    info = museo.descripcion
    info += '<p><a href="' + museo.url + '">Más información</a></p>'
    info += '<b><u>Dirección:</u></b> ' + museo.direccion + '<br/>'
    info += '<b><u>Accesible:</u></b> ' + str(museo.accesibilidad) + '<br/>'
    info += '<b><u>Barrio:</u></b> ' + museo.barrio + '<br/>'
    info += '<b><u>Distrito:</u></b> ' + museo.distrito + '<br/>'
    info += '<b><u>Contacto:</u></b><ul>'
    info += '<li><b><u>Teléfono:</u></b> ' + museo.telefono + '</li>'
    info += '<li><b><u>Email:</u></b> ' + museo.email + '</li></ul>'
    return info

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
    if request.method == 'GET':
        cookies = request.COOKIES
        try:
            accesible = cookies['accesible'] == 'True'
        except KeyError:
            accesible = False

    #museos = update_museos()
    if accesible:
        museos = print_accesibles('')
    else:
        museos = print_museos('')
    usuarios = print_usuarios()
    template = get_template('annotated.html')
    response = HttpResponse(template.render(Context({'title': 'Mis Museos',
                                                 'content': museos + usuarios})))
    if setAccesible:
        response.set_cookie('accesible', value=accesible)
    return response

def museo_all(request):
    if request.method == 'GET':
        cookies = request.COOKIES
        try:
            accesible = cookies['accesible'] == 'True'
        except KeyError:
            accesible = False
        distrito = request.GET.get('distrito', '')

    if accesible:
        museos = print_accesibles(distrito)
    else:
        museos = print_museos(distrito)



    template = get_template('museos.html')
    return HttpResponse(template.render(Context({'title': 'Lista de museos',
                                                'select': select_box(),
                                                'content': museos})))

@csrf_exempt
def museo_id(request, mid):
    try:
        museo = Museo.objects.get(n_id=mid)
        nota = ''

        if request.method == 'POST':
            username = None
            if request.user.is_authenticated():
                username = request.user.username

            comentario = request.POST.get('comentario')
            if comentario == None:
                user = User.objects.get(username=username)
                user = Usuario.objects.get(usuario=user)
                user.usuario_museo.add(museo)
            elif comentario != '':
                comentario = Comentario(username=username, m_id=mid, comentario=comentario)
                comentario.save()
            else:
                nota = 'No se pueden enviar comentarios vacios.<br/><br/>'

        info = print_museo_info(museo)
        comentarios = nota + print_comentarios(mid)

        template = get_template('museo-id.html')
        return HttpResponse(template.render(Context({'title': museo.nombre,
                                                     'content': info,
                                                     'comentarios': comentarios})))

    except Museo.DoesNotExist:
        return HttpResponseNotFound('404 NOT FOUND')

@csrf_exempt
def usuario(request, nombre):
    try:
        usuario = User.objects.get(username=nombre)

        if request.method == 'POST':
            pagina = request.POST.get('pagina', None)
            Usuario.objects.filter(usuario=usuario).update(pagina=pagina)

        usuario = Usuario.objects.get(usuario=usuario)

        n = 0
        if request.method == 'GET':
            n = request.GET.get('show', '0')
            n = int(n)*5

        museos = usuario.usuario_museo.all()
        museos_sliced = museos[n:n+5]
        info = '<b><u>Museos añadidos:</u></b><ul>'
        for museo in museos_sliced:
            info += '<li>' + museo.nombre + '<br/>' + museo.direccion + '<br/>'
            info += '<a href="museos/' + str(museo.n_id) + '">Más información</a><br/><br/>'
        info += '</ul>'

        if n != 0:
            info += '<a href="' + nombre + '?show=' + str(int(n/5)-1) + '">Preview</a>'
        if n+5 < len(museos):
            info += ' <a href="' + nombre + '?show=' + str(int(n/5)+1) + '">Next</a>'

        template = get_template('usuario.html')
        return HttpResponse(template.render(Context({'title': usuario.pagina,
                                                    'content': info})))
    except (User.DoesNotExist, Usuario.DoesNotExist) as e:
        return HttpResponseNotFound('404 NOT FOUND')


def usuario_xml(request, name):
    return HttpResponse('Xml de ' + name)

def about(request):
    return HttpResponse('About')
