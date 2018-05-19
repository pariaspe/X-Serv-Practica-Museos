from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import Museo, Usuario, Comentario, MuseoLike
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Count
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.csrf import csrf_exempt

from xml.sax import make_parser
from urllib import request, error
from xml.sax.handler import ContentHandler
import museos.parser

def print_museos(distrito):
    if distrito == '':
        museos = Museo.objects.all()
    else:
        museos = Museo.objects.filter(distrito=distrito)
    lista = '<ol>'
    for museo in museos:
        lista += '<li><a href="museos/' + str(museo.n_id) + '">' + museo.nombre + '</a></li>'
    lista += '</ol>'
    return lista

def print_accesibles(distrito):
    if distrito == '':
        museos = Museo.objects.filter(accesibilidad=True)
    else:
        museos = Museo.objects.filter(accesibilidad=True).filter(distrito=distrito)
    lista = '<ol>'
    for museo in museos:
        lista += '<li><a href="museos/' + str(museo.n_id) + '">' + museo.nombre + '</a></li>'
    lista += '</ol>'
    return lista

formato_museo = """
<div class="article">
<h2><span><a href="museos/{url}">{name}</a></span></h2>
<p class="info noprint">
    <span class="cat">{direccion}</span><span class="noscreen">,</span>
</p>

<p>{info}</p>

<p class="btn-more box noprint"><strong><a href="museos/{url}">Más</a></strong></p>
</div> <!-- /article -->

<hr class="noscreen" />
"""

def print_most_accesibles(items):
    cont = 0
    lista = ''
    for item in items:
        museo = Museo.objects.get(id=item[0])
        if museo.accesibilidad:
            lista += formato_museo.format(url=str(museo.n_id), name=museo.nombre,
             direccion=museo.direccion, distrito=museo.distrito, info=museo.descripcion)
            cont += 1
            if cont == 5:
                break
    return lista

def print_most(items):
    lista = ''
    for item in items:
        museo = Museo.objects.get(id=item[0])
        lista += formato_museo.format(url=str(museo.n_id), name=museo.nombre,
         direccion=museo.direccion, distrito=museo.distrito, info=museo.descripcion)
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

    return print_museos('')

def print_usuarios():
    usuarios = User.objects.all()
    lista = ''
    for usuario in usuarios:
        try:
            ñoño = Usuario.objects.get(usuario=usuario) # TODO ñoño no es utilizado
            lista += '<li>' + usuario.usuario.pagina + '<a href="' + usuario.username + '">' + usuario.username + '</a></li>'
        except Usuario.DoesNotExist:
            pass
    return lista

def select_box():
    distritos = Museo.objects.all().values_list('distrito', flat=True).distinct()
    select = '<select name="distrito">'
    select += '<option value="">------</option>'
    for distrito in distritos:
        select += '<option value="' + distrito + '">' + distrito + '</option>'
    select += '</select>'
    return select

def print_comentarios(museo):
    comentarios = Comentario.objects.filter(museo=museo)
    info = '<b><u>Comentario:</u></b><br/>'
    for comentario in comentarios:
        info += str(comentario.usuario) + ': ' + comentario.comentario + ' at ' + str(comentario.fecha) + '<br/>'

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

def print_museos_likes(nombre, likes, n):
    likes_sliced = likes[n:n+5]
    info = '<b><u>Museos añadidos:</u></b><ul>'
    for like in likes_sliced:
        museo = like.museo
        fecha = like.fecha
        info += '<li>' + museo.nombre + '<br/>' + museo.direccion + '<br/>'
        info += '<a href="museos/' + str(museo.n_id) + '">Más información</a><br/>'
        info += 'Añadido el: ' + str(fecha) + '</br></br>'
    info += '</ul>'

    if n != 0:
        info += '<a href="' + nombre + '?show=' + str(int(n/5)-1) + '">Preview</a>'
    if n+5 < len(likes):
        info += ' <a href="' + nombre + '?show=' + str(int(n/5)+1) + '">Next</a>'

    return info

# Create your views here.
@csrf_exempt
def barra(request):
    setAccesible = False
    if request.method == 'POST':
        cookies = request.COOKIES
        try:
            accesible = cookies['accesible'] == 'True'
            if request.POST.get('upload'):
                update_museos()
            else:
                accesible = not accesible
                setAccesible = True
        except KeyError:
            accesible = True
            setAccesible = True
    if request.method == 'GET':
        cookies = request.COOKIES
        try:
            accesible = cookies['accesible'] == 'True'
        except KeyError:
            accesible = False

    if accesible:
        comentarios = Comentario.objects.values_list('museo').annotate(comentarios_count=Count('museo')).order_by('-comentarios_count')[:10]
        museos = print_most_accesibles(comentarios)

    else:
        comentarios = Comentario.objects.values_list('museo').annotate(comentarios_count=Count('museo')).order_by('-comentarios_count')[:5]
        museos = print_most(comentarios)

    usuarios = print_usuarios()

    template = get_template('museos/main.html')
    context = Context({'museos': museos,
                       'usuarios': usuarios})
    response = HttpResponse(template.render(context))

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

    template = get_template('museos/museos.html')
    return HttpResponse(template.render(Context({'select': select_box(),
                                                'content': museos})))

@csrf_exempt
def museo_id(request, mid):
    try:
        museo = Museo.objects.get(n_id=mid)
        nota = ''
        username = None

        if request.method == 'POST' and request.user.is_authenticated():
            username = request.user.username
            comentario = request.POST.get('comentario')
            user = User.objects.get(username=username)
            if comentario == None:
                like = MuseoLike(museo=museo, usuario=user.usuario)
                like.save()
            elif comentario != '':
                comentario = Comentario(usuario=user.usuario, museo=museo, comentario=comentario)
                comentario.save()
            else:
                nota = 'No se pueden enviar comentarios vacios.<br/><br/>'

        info = print_museo_info(museo)
        comentarios = nota + print_comentarios(museo)

        if request.user.is_authenticated():
            template = get_template('museos/museo-id-private.html')
        else:
            template = get_template('museos/museo-id.html')
        return HttpResponse(template.render(Context({'title': museo.nombre,
                                                     'content': info,
                                                     'comentarios': comentarios})))

    except Museo.DoesNotExist:
        return HttpResponseNotFound('404 NOT FOUND')

@csrf_exempt
def usuario(request, nombre):
    try:
        usuario = User.objects.get(username=nombre)
        nota = ''
        if request.method == 'POST' and nombre == request.user.username:
            pagina = request.POST.get('pagina', None)
            if pagina != '':
                Usuario.objects.filter(usuario=usuario).update(pagina=pagina)
            else:
                nota = 'El titulo de la pagina no puede estar vacío.</br></br>'

        n = 0
        if request.method == 'GET':
            n = request.GET.get('show', '0')
            n = int(n)*5

        likes = MuseoLike.objects.filter(usuario=usuario.usuario).order_by('-fecha')
        info = print_museos_likes(nombre, likes, n)

        if nombre == request.user.username:
            template = get_template('museos/usuario-private.html')
        else:
            template = get_template('museos/usuario.html')
        return HttpResponse(template.render(Context({'usuario': usuario.username,
                                                    'title': usuario.usuario.pagina,
                                                    'content': nota + info})))
    except (User.DoesNotExist, Usuario.DoesNotExist) as e:
        return HttpResponseNotFound('404 NOT FOUND')


def usuario_xml(request, name):
    return HttpResponse('Xml de ' + name)

def about(request):
    template = get_template('museos/about.html')
    return HttpResponse(template.render(Context({'content': 'About'})))
