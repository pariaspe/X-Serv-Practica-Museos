from .models import Museo, Usuario, Comentario, MuseoLike
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template import Context


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

def print_most_accesibles(items):
    cont = 0
    lista = ''
    template = get_template('formato-museo.html')
    for item in items:
        museo = Museo.objects.get(id=item[0])
        if museo.accesibilidad:
            context = Context({'url': str(museo.n_id), 'name': museo.nombre,
                                'direccion': museo.direccion, 'distrito': museo.distrito, 'info': museo.descripcion})
            lista += template.render(context)
            cont += 1
            if cont == 5:
                break
    return lista

def print_most(items):
    lista = ''
    template = get_template('formato-museo.html')
    for item in items:
        museo = Museo.objects.get(id=item[0])
        context = Context({'url': str(museo.n_id), 'name': museo.nombre,
                            'direccion': museo.direccion, 'distrito': museo.distrito, 'info': museo.descripcion})
        lista += template.render(context)
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
            _ = Usuario.objects.get(usuario=usuario) # El resultado no es utilizado
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

def get_distritos(selected):
    distritos = Museo.objects.all().values_list('distrito', flat=True).distinct()
    lista = ''
    for distrito in distritos:
        if distrito == selected:
            lista += '<li id="category-active"><a href="?distrito=' + distrito + '">' + distrito + '</a></li>'
        else:
            lista += '<li><a href="?distrito=' + distrito + '">' + distrito + '</a></li>'
    return lista

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

def parse_direccion(direccion):
    slices = direccion.split('(')
    via = slices[0]
    slices = slices[1].split(')')
    clase = slices[0]
    slices = slices[1].split()
    num = slices[1]
    localidad = slices[2]
    cp = slices[3]
    return via, clase, num, localidad, cp

def get_museos_xml(likes):
    museos = ''
    template = get_template('museo.xml')
    for like in likes:
        museo = like.museo
        fecha = like.fecha
        accesibilidad = '1' if museo.accesibilidad else '0'
        via, clase, num, localidad, cp = parse_direccion(museo.direccion)
        context = Context({'id': museo.n_id, 'nombre': museo.nombre, 'descripcion': museo.descripcion,
                            'accesibilidad': accesibilidad, 'url': museo.url, 'via': via,
                            'clase': clase, 'num': num, 'localidad': localidad, 'cp': cp, 'barrio': museo.barrio,
                            'distrito': museo.distrito, 'tlf': museo.telefono, 'email': museo.email})
        museos += template.render(context)
    return museos
