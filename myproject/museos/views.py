from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def barra(request):
    return HttpResponse('Barra')

def museos(request):
    return HttpResponse('Museos')

def museo_id(request, mid):
    return HttpResponse('Museo ' + mid)

def usuario(request, name):
    return HttpResponse('Usuario ' + name)

def usuario_xml(request, name):
    return HttpResponse('Xml de ' + name)

def about(request):
    return HttpResponse('About')
