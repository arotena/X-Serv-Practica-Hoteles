"""practica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, patterns, include
from django.contrib import admin

urlpatterns = [
    url(r'^css/style.css$','hoteles.views.servir'),
    url(r'^alojamientos$','hoteles.views.alojamientos'),
    url(r'^alojamientos/(\d+)$','hoteles.views.aloid'),
    url(r'^alojamientos/(\d+)/en$','hoteles.views.ingles'),
    url(r'^alojamientos/(\d+)/fr$','hoteles.views.frances'),
    url(r'^login$', 'django.contrib.auth.views.login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^logout1$', 'django.contrib.auth.views.logout', {'next_page': '/alojamientos'}),
    url(r'^logout2$', 'django.contrib.auth.views.logout', {'next_page': '/about'}),
    url(r'^accounts/profile/$', 'hoteles.views.registrado'),
    url(r'^$' , 'hoteles.views.listar'),
    url(r'^admin/', admin.site.urls),
    url(r'^about$', 'hoteles.views.about'),
    url(r'^add/(\d+)$' , 'hoteles.views.add'),
    url(r'^comentario/(\d+)$' , 'hoteles.views.comentario'),
    url(r'^css$' , 'hoteles.views.css'),
    url(r'^(.+)/mas$' , 'hoteles.views.mas'),
    url(r'^(.+)/menos$' , 'hoteles.views.menos'),
    url(r'^(.+)/xml$' , 'hoteles.views.xml'),
    url(r'^(.+)$' , 'hoteles.views.usuario'),
]
