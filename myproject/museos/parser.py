from xml.sax import make_parser
from urllib import request, error
from xml.sax.handler import ContentHandler

def normalize_whitespace(text):
    "Remove redundant whitespace from a string"
    return ' '.join(text.split())

class CounterHandler(ContentHandler):

    def __init__ (self):
        self.inContent = False
        self.theContent = ''
        self.inItem = False

        self.inNombre = False
        self.nombres = []
        self.inID = False
        self.ids = []
        self.inNombreVia = False
        self.inClaseVia = False
        self.inNum = False
        self.inLocalidad =  False
        self.inPostal = False
        self.direccion = ''
        self.direcciones = []
        self.inDescripcion = False
        self.descripcion = ''
        self.descripciones = []
        self.inAccesibilidad = False
        self.accesibilidad = []
        self.inBarrio = False
        self.barrios = []
        self.inDistrito = False
        self.distritos = []
        self.inUrl = False
        self.urls = []
        self.inTipo = False
        self.contactos = []
        self.inTelefono = False
        self.telefono = ''
        self.inEmail =  False
        self.email = ''
        self.emails = []

    def startElement (self, name, attrs):
        if name == 'atributos':
            self.inItem = True
        elif self.inItem:
            if name == 'atributo':
                title = attrs['nombre']
                if title == 'ID-ENTIDAD':
                    self.inContent = True
                    self.inID = True
                elif title == 'NOMBRE':
                    self.inContent = True
                    self.inNombre = True
                elif title == 'NOMBRE-VIA':
                    self.inContent = True
                    self.inNombreVia = True
                elif title == 'CLASE-VIAL':
                    self.inContent = True
                    self.inClaseVia = True
                elif title == 'NUM':
                    self.inContent = True
                    self.inNum = True
                elif title == 'LOCALIDAD':
                    self.inContent = True
                    self.inLocalidad = True
                elif title == 'CODIGO-POSTAL':
                    self.inContent = True
                    self.inPostal = True
                elif title == 'DESCRIPCION-ENTIDAD':
                    self.inContent = True
                    self.inDescripcion = True
                elif title == 'ACCESIBILIDAD':
                    self.inContent = True
                    self.inAccesibilidad = True
                elif title == 'BARRIO':
                    self.inContent = True
                    self.inBarrio = True
                elif title == 'DISTRITO':
                    self.inContent = True
                    self.inDistrito = True
                elif title == 'CONTENT-URL':
                    self.inContent = True
                    self.inUrl = True
                elif title == 'TELEFONO':
                    self.inContent = True
                    self.inTelefono = True
                elif title == 'EMAIL':
                    self.inContent = True
                    self.inEmail = True
                elif title == 'TIPO':
                    self.inContent = True
                    self.inTipo = True

    def endElement (self, name):
        if self.inContent:
            self.theContent = normalize_whitespace(self.theContent)
        if name == 'atributos':
            self.inItem = False
        if self.inItem:
            if name == 'atributo':
                if self.inID:
                    self.ids.append(self.theContent)
                if self.inNombre:
                    self.nombres.append(self.theContent)
                if self.inDescripcion:
                    self.descripcion = self.theContent
                if self.inNombreVia:
                    self.direccion = self.theContent
                if self.inClaseVia:
                    self.direccion += ' (' + self.theContent + ') '
                if self.inNum:
                    self.direccion += 'NUM ' + self.theContent
                if self.inLocalidad:
                    self.direccion += ', ' + self.theContent + ' '
                if self.inPostal:
                    self.direccion += self.theContent
                    self.direcciones.append(self.direccion)
                    self.direccion = ''
                if self.inAccesibilidad:
                    self.accesibilidad.append(self.theContent)
                    self.descripciones.append(self.descripcion) # Aprovecho este campo posterior que esta en todos los museos para guardar la descripcion
                    self.descripcion = ''
                if self.inBarrio:
                    self.barrios.append(self.theContent)
                if self.inDistrito:
                    self.distritos.append(self.theContent)
                if self.inUrl:
                    self.urls.append(self.theContent)
                if self.inTelefono:
                    self.telefono = self.theContent
                if self.inEmail:
                    self.email = self.theContent
                if self.inTipo: # Aprovecho este campo posterior que esta en todos los museos para guardar los datos de contacto
                    self.contactos.append((self.telefono, self.email))
                    self.telefono = ''
                    self.email = ''


        if self.inContent:
            self.inContent = False
            self.theContent = ''
            self.inNombre = False
            self.inID = False
            self.inNombreVia = False
            self.inClaseVia = False
            self.inNum = False
            self.inLocalidad =  False
            self.inPostal = False
            self.inDescripcion = False
            self.inAccesibilidad = False
            self.inBarrio = False
            self.inDistrito = False
            self.inUrl = False
            self.inTipo = False
            self.inTelefono = False
            self.inEmail =  False

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

if __name__ == '__main__':
    MuseoParser = make_parser()
    MuseoHandler = CounterHandler()
    MuseoParser.setContentHandler(MuseoHandler)

    xmlFile = request.urlopen('https://datos.madrid.es/egob/catalogo/201132-0-museos.xml')
    MuseoParser.parse(xmlFile)

    print('Lista:')
    for i in range(len(MuseoHandler.nombres)):
        print(MuseoHandler.direcciones[i])
    #print(MuseoHandler.direcciones)
    print(len(MuseoHandler.direcciones))
