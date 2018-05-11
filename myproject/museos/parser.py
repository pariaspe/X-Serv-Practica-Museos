from xml.sax import make_parser
from urllib import request, error
from xml.sax.handler import ContentHandler

def normalize_whitespace(text):
    "Remove redundant whitespace from a string"
    return ' '.join(text.split())

class CounterHandler(ContentHandler):

    def __init__ (self):
        self.inContent = False
        self.theContent = ""
        self.inItem = False
        self.inTitle = False
        self.titles = []
        self.inID = False
        self.ids = []
        #self.links = []

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
                    self.inTitle = True
            #elif name == 'link':
            #    self.inContent = 1

    def endElement (self, name):
        if self.inContent:
            self.theContent = normalize_whitespace(self.theContent)
        if name == 'atributos':
            self.inItem = False
        if self.inItem:
            if name == 'atributo':
                if self.inID:
                    self.ids.append(self.theContent)
                if self.inTitle:
                    self.titles.append(self.theContent)


            #elif name == 'link':
            #    self.links.append(self.theContent)
        if self.inContent:
            self.inContent = False
            self.theContent = ""
            self.inTitle = False
            self.inID = False


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
    for i in range(len(MuseoHandler.titles)):
        print(MuseoHandler.titles[i])
    print(MuseoHandler.ids)
    print(MuseoHandler.titles)
