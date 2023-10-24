"""
URL configuration for ISSM_Web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django import views
from django.conf import settings
from django.urls import path, include

import accounts
from .import views
from .views import contacto, vista_reporte

urlpatterns = [
    path('',views.index,name='index'),
    path('listado',views.listado,name='listado'),
    path('nueva/',views.nueva,name='nueva'),
    path('editar/',views.editar,name='editar'),
    path('persona_listado/',views.persona_listado,name='persona_listado'), #lista+buscador
    path('email_comprobante/',views.vista_reporte.as_view(),name='email_comprobante'),
    path('logout/',views.listado,name='logout'),
    path('change_password/',views.change_password,name='change_password'),
    path('contacto/', contacto, name='contacto'),  
    path('editar/<int:cliente_id>/', views.editar, name='editar'),     
]