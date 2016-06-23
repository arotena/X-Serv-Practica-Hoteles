#!/usr/bin/python
# -*- coding: utf-8 -*-
from models import Hoteles, Imagenes
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.hotel = None
        self.img = None
        self.subcat = False
        self.cat = False
    def startElement (self, name, attrs):
        if name == 'basicData':
            self.inItem = True
            self.hotel = Hoteles(nombre="", web="",email="",phone="",body="",address="",country="",categoria="",subcategoria="",nComentario=0)
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'web':
                self.inContent = True
            elif name == 'email':
                self.inContent = True
            elif name == 'phone':
                self.inContent = True
            elif name == 'body':
                self.inContent = True
        if name == 'geoData':
            self.inItem = True
        elif self.inItem:
            if name == 'address':
                self.inContent = True
            elif name == 'country':
                self.inContent = True

        if name =="item":
            if attrs['name']== "SubCategoria":
                self.inContent = True
                self.subcat=True;
        if name =="item":
            if attrs['name']== "Categoria":
                self.inContent = True
                self.cat=True;

        if name == 'multimedia':
            self.inItem = True
        elif self.inItem:
            if name == 'url':
                self.inContent = True

    def endElement (self, name):
        if name == 'basicData':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.hotel.nombre = self.theContent
                self.hotel.save()
                self.inContent = False
                self.theContent = ""
            elif name == 'web':
                self.hotel.web = self.theContent
                self.hotel.save()
                self.inContent = False
                self.theContent = ""
            elif name == 'email':
                self.hotel.email = self.theContent
                self.hotel.save()
                self.inContent = False
                self.theContent = ""
            elif name == 'phone':
                self.hotel.phone = self.theContent
                self.hotel.save()
                self.inContent = False
                self.theContent = ""
            elif name == 'body':
                self.hotel.body = self.theContent
                self.hotel.save()
                self.inContent = False
                self.theContent = ""

        if name == 'geoData':
            self.inItem = False
        elif self.inItem:
            if name == 'address':
                self.hotel.address = self.theContent
                self.hotel.save()
                self.inContent = False
                self.theContent = ""
            elif name == 'country':
                self.hotel.country = self.theContent
                self.hotel.save()
                self.inContent = False
                self.theContent = ""
        if name == 'item' and self.subcat:
                self.hotel.subcategoria = self.theContent
                self.hotel.save()
                self.subcat = False
                self.inContent = False
                self.theContent = ""
        if name == 'item' and self.cat:
                self.hotel.categoria = self.theContent
                self.hotel.save()
                self.cat = False
                self.inContent = False
                self.theContent = ""

        if name == 'multimedia':
            self.inItem = False
        elif self.inItem:
            if name == 'url':
                self.img=Imagenes(src="",hotel=self.hotel)
                self.img.src = self.theContent
                self.img.save()
                self.inContent = False
                self.theContent = ""
                self.unica = False

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars
