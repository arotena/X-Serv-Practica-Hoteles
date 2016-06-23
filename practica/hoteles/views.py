from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.template import Context
from django.template.loader import get_template
from django.template import RequestContext
from claseparser import myContentHandler
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
import urllib2
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
from models import Hoteles, Imagenes, Colecciones, Comentarios, Css
from lxml import etree
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
# Create your views here.
min = 0
max = 10
@csrf_exempt
def listar(request):
    global min,max
    min=0
    max=10
    listado = Hoteles.objects.all().order_by("-nComentario")
    imagen = Imagenes.objects.all()
    comentados = False
    if request.method == "POST":
        if len(listado) == 0 and len(imagen) == 0:
            theParser = make_parser()
            theHandler = myContentHandler()
            theParser.setContentHandler(theHandler)
            response = urllib2.urlopen('http://cursosweb.github.io/etc/alojamientos_es.xml')
            theParser.parse(response)
            listado = Hoteles.objects.all().order_by("-nComentario")
            imagen = Imagenes.objects.all()
    if len(listado) == 0 and len(imagen) == 0:
        cont = '<form method="post" action="/">'
        cont += '<input type="submit" value="Cargar Hoteles" /></form>'
    else:
        cont = ' <div id="alojamientos" style="overflow-y:auto;height: 400px;width:60%;text-align:center">'
        n = 0;
        for elemento in listado:
            if n==10:
                break
            if elemento.nComentario != 0:
                comentados = True;
                cont += '<div style="border-radius: 5px;border: 3px solid black;"><a href ="'+str(elemento.web)+'">' + str(elemento.nombre) + "</a></br>"
                cont +=  unicode(elemento.address).encode('utf-8') + "."+ str(elemento.country) + "</br>"
                encontrada = Imagenes.objects.filter(hotel=elemento.id)
                if len(encontrada) != 0:
                    cont += '<img style="height: 30%;width:40%" src="'+str(encontrada[0].src)+'"></img>'
                else:
                    pass
                cont += '<a href="alojamientos/'+str(elemento.id)+'">Mas Informacion</a></br></div>'
            n = n + 1
        if(comentados == False):
            cont += "<h4>No hay alojamientos comentados</h4>"
        cont += "</div>"
        cont += '<div id="paguser"style="overflow-y:auto;height: 400px">'
        usuarios = username=User.objects.all()
        for usuario in usuarios:
            try:
                user_owner=Css.objects.get(usuario=usuario)
                cont+= '<a href="'+str(user_owner.usuario)+'">' + unicode(user_owner.title).encode('utf-8')
            except Css.DoesNotExist:
                cont+= '<a href="'+str(usuario.username)+'">Pagina de ' + str(usuario.username)
            cont+= '</a> ('+str(usuario.username)+')</br>'
        cont += '</div>'
    if request.user.is_authenticated():
        user = request.user.username
        argumentos = {'contenido': cont,'usuario':user}
        return  render_to_response('principal.html', argumentos, context_instance = RequestContext(request))
    argumentos = {'contenido': cont}
    return render_to_response('principal.html', argumentos, context_instance = RequestContext(request))

@csrf_exempt
def alojamientos(request):
    listado = Hoteles.objects.all()
    cont = ""
    if len(listado) != 0:
        if request.method == "POST":
            cat = request.POST.get('cat')
            sub = request.POST.get('sub')
            encontrada = Hoteles.objects.filter(categoria=cat,subcategoria=sub)

            if len(encontrada) != 0:
                for elemento in encontrada:
                    cont += '<a href ="alojamientos/'+str(elemento.id)+'">' + str(elemento.nombre) + "</a></br>"
            else:
                cont += "<h5>No se ha encontrado coincidencias</h5>"
        else:
            for elemento in listado:
                cont += '<a href ="alojamientos/'+str(elemento.id)+'">' + str(elemento.nombre) + "</a></br>"
    else:
        cont += "<p>Carga los alojamientos</p>"

    if request.user.is_authenticated():
        user = request.user.username
        argumentos = {'contenido': cont,'usuario':user}
        return  render_to_response('alojamientos.html', argumentos, context_instance = RequestContext(request))
    argumentos = {'contenido': cont}
    return render_to_response('alojamientos.html', argumentos, context_instance = RequestContext(request))


@csrf_exempt
def aloid(request,id):
    cont = "<div id='hotel'>"
    try:
        encontrada = Hoteles.objects.get(id=id)
        cont += "<h2>" + str(encontrada.nombre) + "</h2><p>"
        cont += unicode(encontrada.address).encode('utf-8') + "." + str(encontrada.country)+"</br>"
        cont += "email: "+unicode(encontrada.email).encode('utf-8') + "</br>Tel:"+unicode(encontrada.phone).encode('utf-8') + "</p>"
        cont += '<a href="'+str(encontrada.web)+'">Web</a>'
        cont += "<p>"+unicode(encontrada.body).encode('utf-8')+"</p>"
        imagenes = Imagenes.objects.filter(hotel=encontrada.id)
        if len(imagenes) != 0:
            for elemento in imagenes:
                cont += "<img class='imgalo' src='"+str(elemento.src)+"'></img>"
        else:
            pass
        cont += '</br>'
        comentarios=Comentarios.objects.filter(hotel=id)
        coment = '<div id="coments"><h1>Comentarios:</h1>'
        if len(comentarios) != 0:
            for comentario in comentarios:
                coment+="<div style='border-radius: 5px;border: 3px solid black;'>"
                coment+="<h3>"+str(comentario.usuario)+":</h3>"
                coment+="<p>"+unicode(comentario.contenido).encode('utf-8')+"</p></div>"
        else:
            coment += "Este alojamiento no tiene comentarios"
        coment += "</div>"
    except Hoteles.DoesNotExist:
        cont += "<h1>No se ha encontrado dicho alojamiento</h1>"
    cont+="</div>"
    if request.user.is_authenticated():
        user = request.user.username
        add='<form action="/add/'+str(id)+'" method="POST" >'
        add+= '<p><input id="anadir"type="submit" value="Add a Colecciones"></p></form>'
        idioma = '<div id="idiomas"><a href="/alojamientos/'+str(id)+'/en">English</a>'
        idioma += '<a style="margin-left:10px" href="/alojamientos/'+str(id)+'/fr">French</a>'
        idioma += '<a style="margin-left:10px" href="/alojamientos/'+str(id)+'">Spanish</a></div>'
        comentario='<div id="comentario"><form id="formu" action="/comentario/'+str(id)+'" method="POST" >'
        comentario += 'Comentario:</br><textarea name="comentario" rows="10" cols="40"placeholder="Comentario"></textarea>'
        comentario+= '</br><input id="enviar"type="submit" value="Enviar"></form></div>'
        argumentos = {'contenido': cont,'usuario':user,'add':add,'comentario':comentario,'opiniones':coment,'idiomas':idioma}
        return  render_to_response('alo.html', argumentos, context_instance = RequestContext(request))
    argumentos = {'contenido': cont,'comentario':"Registrate para poder poner comentarios",'opiniones':coment}
    return render_to_response('alo.html', argumentos, context_instance = RequestContext(request))
@csrf_exempt
def ingles(request,idhotel):
    doc = etree.parse('http://cursosweb.github.io/etc/alojamientos_en.xml')
    raiz=doc.getroot()
    encontrado = False
    cont = "<div id='hotel'>"
    try:
        hotel = Hoteles.objects.get(id=idhotel)
        for hxml in raiz.iter("basicData"):
            nombre = hxml.find("name").text
            if nombre == hotel.nombre:
                encontrado = True;
                body=hxml.find("body").text
                phone=hxml.find('phone').text
                email=hxml.find('email').text
                web=hxml.find('web').text
                break
        if encontrado == True:
            for loca in raiz.iter('geoData'):
                address=loca.find('address').text
                country=loca.find('country').text
                break
            cont += "<h2>" + str(nombre) + "</h2><p>"
            cont += unicode(address).encode('utf-8') + "." + str(country)+"</br>"
            cont += "email: "+unicode(email).encode('utf-8') + "</br>Tel:"+unicode(phone).encode('utf-8') + "</p>"
            cont += '<a href="'+str(web)+'">Web</a>'
            cont += "<p>"+unicode(body).encode('utf-8')+"</p>"
            imagenes = Imagenes.objects.filter(hotel=idhotel)
            if len(imagenes) != 0:
                for elemento in imagenes:
                    cont += "<img class='imgalo' src='"+str(elemento.src)+"'></img>"
            else:
                pass
            cont += '</br>'
        else:
            cont += "<h2>" + str(hotel.nombre) + "</h2><p>"
            cont += "Este alojamiento no esta disponible en este idioma</p>"
        comentarios=Comentarios.objects.filter(hotel=idhotel)
        coment = '<div id="coments"><h1>Comentarios:</h1>'
        if len(comentarios) != 0:
            for comentario in comentarios:
                coment+="<div style='border-radius: 5px;border: 3px solid black;'>"
                coment+="<h3>"+str(comentario.usuario)+":</h3>"
                coment+="<p>"+unicode(comentario.contenido).encode('utf-8')+"</p></div>"
        else:
            coment += "Este alojamiento no tiene comentarios"
        coment += "</div>"
    except User.DoesNotExist:
        cont += "<h1>No se ha encontrado dicho alojamiento</h1>"
    cont+="</div>"
    cont+="</div>"
    if request.user.is_authenticated():
        user = request.user.username
        add='<form action="/add/'+str(idhotel)+'" method="POST" >'
        add+= '<p><input id="anadir"type="submit" value="Add a Colecciones"></p></form>'
        idioma = '<div id="idiomas"><a href="/alojamientos/'+str(idhotel)+'/en">English</a>'
        idioma += '<a style="margin-left:10px" href="/alojamientos/'+str(idhotel)+'/fr">French</a>'
        idioma += '<a style="margin-left:10px" href="/alojamientos/'+str(idhotel)+'">Spanish</a></div>'
        comentario='<div id="comentario"><form id="formu" action="/comentario/'+str(idhotel)+'" method="POST" >'
        comentario += 'Comentario:</br><textarea name="comentario" rows="10" cols="40"placeholder="Comentario"></textarea>'
        comentario+= '</br><input id="enviar"type="submit" value="Enviar"></form></div>'
        argumentos = {'contenido': cont,'usuario':user,'add':add,'comentario':comentario,'opiniones':coment,'idiomas':idioma}
        return  render_to_response('alo.html', argumentos, context_instance = RequestContext(request))
    argumentos = {'contenido': cont,'comentario':"Registrate para poder poner comentarios",'opiniones':coment}
    return render_to_response('alo.html', argumentos, context_instance = RequestContext(request))
@csrf_exempt
def frances(request,idhotel):
    doc = etree.parse('http://cursosweb.github.io/etc/alojamientos_fr.xml')
    raiz=doc.getroot()
    encontrado = False
    cont = "<div id='hotel'>"
    try:
        hotel = Hoteles.objects.get(id=idhotel)
        for hxml in raiz.iter("basicData"):
            nombre = hxml.find("name").text
            if nombre == hotel.nombre:
                encontrado = True;
                body=hxml.find("body").text
                phone=hxml.find('phone').text
                email=hxml.find('email').text
                web=hxml.find('web').text
                break
        if encontrado == True:
            for loca in raiz.iter('geoData'):
                address=loca.find('address').text
                country=loca.find('country').text
                break
            cont += "<h2>" + str(nombre) + "</h2><p>"
            cont += unicode(address).encode('utf-8') + "." + str(country)+"</br>"
            cont += "email: "+unicode(email).encode('utf-8') + "</br>Tel:"+unicode(phone).encode('utf-8') + "</p>"
            cont += '<a href="'+str(web)+'">Web</a>'
            cont += "<p>"+unicode(body).encode('utf-8')+"</p>"
            imagenes = Imagenes.objects.filter(hotel=idhotel)
            if len(imagenes) != 0:
                for elemento in imagenes:
                    cont += "<img class='imgalo' src='"+str(elemento.src)+"'></img>"
            else:
                pass
            cont += '</br>'
        else:
            cont += "<h2>" + str(hotel.nombre) + "</h2><p>"
            cont += "Este alojamiento no esta disponible en este idioma</p>"
        comentarios=Comentarios.objects.filter(hotel=idhotel)
        coment = '<div id="coments"><h1>Comentarios:</h1>'
        if len(comentarios) != 0:
            for comentario in comentarios:
                coment+="<div style='border-radius: 5px;border: 3px solid black;'>"
                coment+="<h3>"+str(comentario.usuario)+":</h3>"
                coment+="<p>"+unicode(comentario.contenido).encode('utf-8')+"</p></div>"
        else:
            coment += "Este alojamiento no tiene comentarios"
        coment += "</div>"
    except User.DoesNotExist:
        cont += "<h1>No se ha encontrado dicho alojamiento</h1>"
    cont+="</div>"
    cont+="</div>"
    if request.user.is_authenticated():
        user = request.user.username
        add='<form action="/add/'+str(idhotel)+'" method="POST" >'
        add+= '<p><input id="anadir"type="submit" value="Add a Colecciones"></p></form>'
        idioma = '<div id="idiomas"><a href="/alojamientos/'+str(idhotel)+'/en">English</a>'
        idioma += '<a style="margin-left:10px" href="/alojamientos/'+str(idhotel)+'/fr">French</a>'
        idioma += '<a style="margin-left:10px" href="/alojamientos/'+str(idhotel)+'">Spanish</a></div>'
        comentario='<div id="comentario"><form id="formu" action="/comentario/'+str(idhotel)+'" method="POST" >'
        comentario += 'Comentario:</br><textarea name="comentario" rows="10" cols="40"placeholder="Comentario"></textarea>'
        comentario+= '</br><input id="enviar"type="submit" value="Enviar"></form></div>'
        argumentos = {'contenido': cont,'usuario':user,'add':add,'comentario':comentario,'opiniones':coment,'idiomas':idioma}
        return  render_to_response('alo.html', argumentos, context_instance = RequestContext(request))
    argumentos = {'contenido': cont,'comentario':"Registrate para poder poner comentarios",'opiniones':coment}
    return render_to_response('alo.html', argumentos, context_instance = RequestContext(request))
@csrf_exempt
def usuario(request,nombre):
    try:
        username=User.objects.get(username=nombre)
    except User.DoesNotExist:
        cont='Este usuario no existe '
        argumentos = {'contenido': cont}
        return  render_to_response('userno.html', argumentos, context_instance = RequestContext(request))
    try:
        user_owner=Css.objects.get(usuario=nombre)

        cont = '<h1>'+unicode(user_owner.title).encode('utf-8')+'</h1></br>'
    except Css.DoesNotExist:
        cont = '<h1>Pagina de '+str(username)+"</h1></br>"
    cont += '<div id="coleccion">'
    coleccion = Colecciones.objects.filter(usuario=username)
    n = 0
    global min,max
    if len(coleccion) != 0:
        cont += '<a href="'+str(username)+'/xml">XML</a>'
        new_coleccion = coleccion[min:max]
        if len(new_coleccion) == 0:
            min = 0
            max = 10
            new_coleccion = coleccion[min:max]
        for hotel in coleccion:
            if n>=max:
                cont += '<a href="'+str(nombre)+'/mas">Mas</a>'
                break
            if n==0:
                for aloja in new_coleccion:
                    try:
                        elemento = Hoteles.objects.get(id=aloja.alojamiento)
                        cont += '<div style="border-radius: 5px;border: 3px solid black;"><a href ="'+str(elemento.web)+'">' + str(elemento.nombre) + "</a></br>"
                        cont +=  unicode(elemento.address).encode('utf-8') + "."+ str(elemento.country) + "</br>"
                        encontrada = Imagenes.objects.filter(hotel=elemento.id)
                        if len(encontrada) != 0:
                            cont += '<img style="height: 20%;width:40%" src="'+str(encontrada[0].src)+'"></img>'
                        else:
                            pass
                        cont += '<a href="alojamientos/'+str(elemento.id)+'">Mas Informacion</a></br>'

                        cont += str(aloja.date) + "</div>"
                    except Hoteles.DoesNotExist:
                        pass
                if min >= 10:
                    cont += '<a style="margin-right:5px;"href="'+str(nombre)+'/menos">Atras</a>'
            n = n+1
    else:
        cont+='<h4>Este usuario no tiene alojamientos en sus colecciones</h4>'
    cont +="</div>"
    if request.user.is_authenticated():
        user = request.user.username
        argumentos = {'contenido': cont,'usuario':user}
        if str(user)==str(username) :
            formulario = '<h3>Elige tu css:</h3>'
            formulario += '<div id="css"><form action = "/css" method="POST">'
            formulario += '<br>Titulo:<input type="text" name="title">'
            formulario+='<br>Background-color:<input type="text" name="color">'
            formulario += '<br>Font-size:<input type="text" name="sizef"><br><input type="submit" value="Guardar"></form></div>'
            argumentos = {'contenido': cont,'usuario':user,'formu':formulario}

    else:
        argumentos = {'contenido': cont}
    return  render_to_response('userno.html', argumentos, context_instance = RequestContext(request))
@csrf_exempt
def mas(request,usuario):
    global min, max
    min +=10
    max +=10
    return HttpResponseRedirect('/'+str(usuario))
@csrf_exempt
def menos(request,usuario):
    global min, max
    if min >= 10:
        min -=10
    if max >= 20:
        max -=10
    return HttpResponseRedirect('/'+str(usuario))
@csrf_exempt
def xml(request,usuario):
    try:
        username=User.objects.get(username=usuario)
    except User.DoesNotExist:
        return HttpResponseRedirect('/'+str(usuario))
    coleccion = Colecciones.objects.filter(usuario=username)
    if(len(coleccion)!=0):
        root = ET.Element("coleccion")
        for hotel in coleccion:
            try:
                elemento = Hoteles.objects.get(id=hotel.alojamiento)
                doc = ET.SubElement(root, "alojamiento")
                doc1 = ET.SubElement(doc, "basicData")
                ET.SubElement(doc1, "title").text = elemento.nombre
                ET.SubElement(doc1, "web").text = elemento.web
                ET.SubElement(doc1, "phone").text = elemento.phone
                ET.SubElement(doc1, "email").text = elemento.email
                ET.SubElement(doc1, "body").text = elemento.body
                doc2 = ET.SubElement(doc, "geoData")
                ET.SubElement(doc2, "address").text = elemento.address
                ET.SubElement(doc2, "country").text = elemento.country
                doc3 = ET.SubElement(doc, "multimedia")
                encontrada = Imagenes.objects.filter(hotel=elemento.id)
                if len(encontrada) != 0:
                    for imagen in encontrada:
                        ET.SubElement(doc3, "url").text = imagen.src
                else:
                    pass
                doc4 = ET.SubElement(doc, "extradata")
                ET.SubElement(doc4, "item", name="Categoria").text = elemento.categoria
                ET.SubElement(doc4, "item", name="SubCategoria").text = elemento.subcategoria
            except Hoteles.DoesNotExist:
                pass
        xmlstr = tostring(root)
        return HttpResponse(xmlstr,content_type='text/xml')
    return HttpResponseRedirect('/'+str(usuario))
@csrf_exempt
def css(request):
    if request.method == "POST":
        if request.user.is_authenticated():
            user = request.user.username
            color = request.POST['color']
            size = request.POST['sizef']
            titulo = request.POST['title']
            if color == "":
                color="white"
            if size == "":
                size = "1em"
            if titulo == "":
                titulo = "Pagina de "+str(user)
            try:
                user_css = Css.objects.get(usuario = user)
                user_css.color = color
                user_css.size = size
                user_css.title = titulo
                user_css.save()
            except Css.DoesNotExist:
                elemento = Css(usuario=user,color=color,size=size,title=titulo)
                elemento.save()
    return HttpResponseRedirect('/')
@csrf_exempt
def add(request,idhotel):
    encontrado=False
    if request.method == "POST":
        if request.user.is_authenticated():
            user = request.user.username
            coleccion = Colecciones.objects.filter(usuario=user)
            if len(coleccion) != 0:
                for elemento in coleccion:
                    if elemento.alojamiento == idhotel:
                        encontrado=True
                        break
            else:
                pass
            if encontrado==False:
                elemento = Colecciones(usuario=user,alojamiento=idhotel)
                elemento.save()
    return HttpResponseRedirect('/alojamientos/'+idhotel)
@csrf_exempt
def comentario(request,idhotel):
    encontrado=False
    if request.method == "POST":
        if request.user.is_authenticated():
            user = request.user.username
            comentarios = Comentarios.objects.filter(usuario=user)
            if len(comentarios) != 0:
                for comentario in comentarios:
                    if comentario.hotel == idhotel:
                        encontrado=True
                        break
            else:
                pass
            if encontrado==False:
                cont = request.POST['comentario']
                elemento = Comentarios(usuario=user,contenido=cont,hotel=idhotel)
                elemento.save()
                hotel = Hoteles.objects.get(id=idhotel)
                hotel.nComentario = hotel.nComentario + 1
                hotel.save()
            else:
                cont = request.POST['comentario']
                coment = Comentarios.objects.get(usuario=user,hotel=idhotel)
                coment.contenido = cont
                coment.save()
    return HttpResponseRedirect('/alojamientos/'+idhotel)
@csrf_exempt
def servir(request):
    if request.user.is_authenticated():
        user = request.user.username
        try:
            user_css = Css.objects.get(usuario = user)
            argumentos = {'fondo':user_css.color,'size':user_css.size}
        except Css.DoesNotExist:
            argumentos = {'fondo':"white",'size':"1em"}
    else:
        argumentos = {'fondo':"white",'size':"1em"}
    template = get_template("style.css")
    return HttpResponse(template.render(argumentos),content_type="text/css")
@csrf_exempt
def about(request):
    cont = '<h1>Funcionalidad de la practica:</h1>'
    cont += '<h4 style="text-decoration:underline;">Usuarios no registrados:</h4>'
    cont += '<p>Estos usuarios solo pueden ver la parte publica que consiste en:</p>'
    cont += '<ul><li>Ver los hoteles mas comentados</li><li>Visitar las paginas de los usuarios de la aplicacion</li>'
    cont += '<li>Ver el XML de la coleccion de cada usuario</li>'
    cont += '<li>Filtrar los hoteles por categoria y subcategoria</li><li>Permite ver los '
    cont += 'comentarios de los usuarios en los alojamientos</li></ul>'
    cont += '<h4 style="text-decoration:underline;">Usuarios registrados:</h4>'
    cont += '<p>Estos usuarios ademas de la parte publica pueden:</p>'
    cont += '<ul><li>Poner comentarios en los alojamientos</li>'
    cont += '<li>Personalizar la pagina cambiando el valor del css</li>'
    cont += '<li>Agregar alojamientos a tu coleccion de alojamientos</li>'
    cont += '<li>Ver la Informacion del alojamiento en varios idiomas</li></ul>'
    if request.user.is_authenticated():
        user = request.user.username
        argumentos = {'contenido': cont,'usuario':user}
        return  render_to_response('about.html', argumentos, context_instance = RequestContext(request))
    argumentos = {'contenido': cont}
    return  render_to_response('about.html', argumentos, context_instance = RequestContext(request))
def registrado(request):
    return HttpResponseRedirect('/')
