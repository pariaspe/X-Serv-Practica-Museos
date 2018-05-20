from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from .models import Museo, Usuario, Comentario, MuseoLike
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Count
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
import datetime

from xml.sax import make_parser
from urllib import request, error
from xml.sax.handler import ContentHandler
import museos.parser
from museos.utils import *

# Create your views here.
@csrf_exempt
def barra(request):
    setAccesible = False
    error_login = False
    error_created = False
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
        error_login = request.GET.get('login', '') == 'False'
        error_created = request.GET.get('created', '') == 'False'

    alert = ''
    if error_login:
        alert = '<script type="text/javascript">alert("Usuario no registrado.");</script>'
    elif error_created:
        alert = '<script type="text/javascript">alert("El usuario ya existe.");</script>'


    if accesible:
        comentarios = Comentario.objects.values_list('museo').annotate(comentarios_count=Count('museo')).order_by('-comentarios_count')[:10]
        museos = print_most_accesibles(comentarios)

    else:
        comentarios = Comentario.objects.values_list('museo').annotate(comentarios_count=Count('museo')).order_by('-comentarios_count')[:5]
        museos = print_most(comentarios)

    usuarios = print_usuarios()

    template = get_template('museos/main.html')
    context = Context({'aut': request.user.is_authenticated(),
                       'name': request.user.username,
                       'museos': museos,
                       'alert': alert,
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
    return HttpResponse(template.render(Context({'aut': request.user.is_authenticated(),
                                                'name': request.user.username,
                                                'select': select_box(),
                                                'distritos': get_distritos(distrito),
                                                'content': museos})))

def usuario_all(request):
    template = get_template('museos/usuarios.html')
    return HttpResponse(template.render(Context({'aut': request.user.is_authenticated(),
                                                'name': request.user.username,
                                                'content': print_usuarios()})))

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

        template = get_template('museos/museo-id.html')
        return HttpResponse(template.render(Context({'aut': request.user.is_authenticated(),
                                                     'name': request.user.username,
                                                     'title': museo.nombre,
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
            tam = request.POST.get('tam', None)
            color = request.POST.get('color', None)
            if pagina != '' and pagina != None:
                Usuario.objects.filter(usuario=usuario).update(pagina=pagina)
            elif tam != '' and tam != None:
                Usuario.objects.filter(usuario=usuario).update(tam_letra_css=tam)
                if color != '' and color != None:
                    Usuario.objects.filter(usuario=usuario).update(color_fondo_css=color)
            elif color != '' and color != None:
                    Usuario.objects.filter(usuario=usuario).update(color_fondo_css=color)
            else:
                nota = 'Los campos para cambiar la configuracion no puede estar vacío.</br></br>'

        n = 0
        if request.method == 'GET':
            n = request.GET.get('show', '0')
            n = int(n)*5

        cookies = request.COOKIES
        try:
            accesible = cookies['accesible'] == 'True'
        except KeyError:
            accesible = False

        if accesible:
            likes = MuseoLike.objects.filter(usuario=usuario.usuario).filter(museo__accesibilidad=True).order_by('-fecha')
        else:
            likes = MuseoLike.objects.filter(usuario=usuario.usuario).order_by('-fecha')

        info = print_museos_likes(nombre, likes, n)

        template = get_template('museos/usuario.html')
        return HttpResponse(template.render(Context({'aut': request.user.is_authenticated(),
                                                    'name': request.user.username,
                                                    'usuario': usuario.username,
                                                    'title': usuario.usuario.pagina,
                                                    'author': nombre == request.user.username,
                                                    'content': nota + info})))
    except (User.DoesNotExist, Usuario.DoesNotExist) as e:
        return HttpResponseNotFound('404 NOT FOUND')

def usuario_xml(request, name):
    template = get_template('base.xml')
    usuario = User.objects.get(username=name)
    likes = MuseoLike.objects.filter(usuario=usuario.usuario).order_by('-fecha')
    content = get_museos_xml(likes)
    context = Context({'usuario': name, 'fecha': datetime.datetime.now(), 'creador': request.user.username, 'content': content})
    return HttpResponse(template.render(context), content_type='text/xml')

def about(request):
    template = get_template('museos/about.html')
    return HttpResponse(template.render(Context({'aut': request.user.is_authenticated(),
                                                'name': request.user.username})))

@csrf_exempt
def login_user(request):
    user = None
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if request.POST['login'] == 'New':
            try:
                user = User.objects.create_user(username, '', password)
                user.save()
            except IntegrityError:
                error = '?created=False'
        else:
            user = authenticate(username=username, password=password)

    if user is None:
        if error == '':
            return HttpResponseRedirect('/?login=False')
        else:
            return HttpResponseRedirect('/' + error)
    else:
        login(request, user)
        return HttpResponseRedirect('/')

def style(request):
    try:
        user = User.objects.get(username=request.user.username)
        tam = user.usuario.tam_letra_css
        color = user.usuario.color_fondo_css
    except User.DoesNotExist:
        tam = 11 # Valor por defecto
        color = 'rgb(242, 245, 254)' # Valor por defecto
    style = get_template('museos/style.css')
    style = style.render(Context({'tam': tam, 'color': color}))
    return HttpResponse(style, content_type='text/css')
