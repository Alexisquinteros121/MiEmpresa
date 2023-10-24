import datetime
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .pdf import render_to_pdf
from .forms import ContactoForm, FormPersona
from .models import Persona, Titular
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView
import os
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend


def index(request):
    return render(request,'personas/base.html')

def listado(request):
    personas= Persona.objects.all()
    return render(request,'personas/listado.html',{'personas':personas})

def editar(request,id):
    persona = get_object_or_404(Persona,pk=id)
    if request.method=="POST":
        formpersona = FormPersona(request.POST,instance=persona)
        if formpersona.is_valid():
            formpersona.save()
            return redirect('personas/editar.html')
    else:
        formpersona = FormPersona(instance=persona)
        return render(request,'persona/editar.html',{'formpersona':formpersona})
    
def nueva(request):
    if request.method == 'POST':
    
        formpersona=FormPersona(request.POST, request.FILES)
        if formpersona.is_valid():
            formpersona.save()
            return redirect('listado')
        else:
            messages.error(request, 'Hubo un error en la operación.')
            
    else:
        formpersona=FormPersona()
    return render(request,'personas/nuevo.html',{'formpersona':formpersona})

def persona_listado(request):
    busqueda = request.POST.get('buscar')
    personas= Persona.objects.all().order_by('apellido','nombre')
    cantidad = len(personas)
    encontrados = cantidad
    if busqueda:
        personas= Persona.objects.filter(
            Q(dni_icontains=busqueda) |
            Q(apellido_icontains=busqueda)|
            Q(nombre_icontains=busqueda) |
            Q(email_icontains=busqueda)
            ).distinct().order_by('apellido','nombre')
        encontrados=len(personas)
    return render(request,'persona/persona_lista.html',
                  {"personas":personas,
                   "cantidad": cantidad,
                   "encontrados": encontrados})
# Create your views here.
class vista_reporte(View):
    def get(self,request,*args,**kwrags):
        try:
            persona_listado=Persona.objects.all()
            template=get_template('personas/reporte_personas.html')
            context= {'title': 'Mi primer pdf','persona_listado':persona_listado}
            html= template.render(context)
            response= HttpResponse(content_type='application/pdf')
            response['Content-Disposition']='attachment; filename="report.pdf" '
            pisaStatus= pisa.CreatePDF(
                html, dest=response
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('vista_reporte'))

@login_required
def change_password(request):
    return PasswordChangeView.as_view(
        template_name='registration/change_password.html',
        SUCCESS_url=reverse_lazy('index'))(request)




#ENVIAR EMAIL
class email_comprobante(View): 
    def link_callback(self, uri, rel):
        sUrl = settings.STATIC_URL 
        sRoot = settings.STATIC_ROOT 
        mUrl = settings.MEDIA_URL 
        mRoot = settings.MEDIA_ROOT
        if uri.startswith(mUrl):            
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri
        if not os.path.isfile(path):
            raise Exception('media URI must start with %s or %s' % (sUrl, mUrl)) 
        return path
    

def get(self, request, id, **kwargs):
    try:
        fecha_actual = datetime.datetime.now()
        usuario = request.user
        template = get_template('ISSM_Web/pdf_seguro_todos.html')
        titular = Titular
        if titular.email:
            #beneficiarios = Beneficiario.objects.filter(titular=titular).order_by()
            print('Encontró Titular')
            context = {
                'titular': titular,
                'usuario': usuario,
                'fecha_actual': fecha_actual,
                #'beneficiarios': beneficiarios,
                #'logo': '{}{}'.format(settings.STATIC_URL, 'assets/img/logo_horizontal.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)

            if pisa_status.err:
                return HttpResponse('Error al generar el PDF', status=500)

            # Enviamos el correo electrónico con el PDF adjunto
            mensaje_email = "Se envía informe de las personas registradas \n Cordiales Saludos"
            if titular.sexo == 'Femenino':
                membresia = "Estimada " + titular.nombre + ", " + titular.apellido + "\n \n"
            else:
                membresia = "Estimado " + titular.nombre + ", " + titular.apellido + "\n \n"
            Asunto_del_correo = 'INFORME DE CLIENTES'
            pie_del_correo = '\n\n\nEste mail es enviado automáticamente. Por favor, no lo respondas\nEstás recibiendo este mensaje porque has estado en contacto con la CAJA DE CREDITOS Y PRESTACIONES CATAMARCA'
            Cuerpo_del_correo = membresia + mensaje_email + pie_del_correo
            email = EmailMessage(Asunto_del_correo, Cuerpo_del_correo, settings.EMAIL_HOST_USER, [titular.email])
            email.attach('INFORME_PERSONAS_REGISTRADAS.pdf', response.getvalue(), 'application/pdf')
            email.send()
            # return HttpResponse('Correo enviado con éxito.')
            messages.success(request, 'Correo enviado con éxito.')
        else:
            messages.error(request, 'Atención: El Titular ' + titular.apellido + 'No tiene Registrado un EMAIL')
    except Exception as e:
        # Manejar errores
        messages.error(request, 'Atención: Verifique la conexión a Internet')
    return redirect('titulares')

    
def contacto(request):
    form_contacto= ContactoForm()
    if request.method == 'POST':
        form_contacto = ContactoForm(request.POST)
        if form_contacto.is_valid():
            nombre = request.POST['nombre']
            email = request.POST['email']
            mensaje = request.POST['mensaje']
       
             # Envía el correo electrónico
            send_mail(
                'Contacto - Alexis Quinteros',
                f'Nombre: {nombre}\nEmail: {email}\nMensaje: {mensaje}',
                'tu_email@dominio.com',  # Dirección de correo electrónico del remitente
                [''],  # Lista de destinatarios o solo 1
                fail_silently=False,
            )
            messages.success(request, 'Correo enviado con éxito.')
        else:
            messages.error('Error. Por favor verifica que los datos esten correctos.') 
        # Lógica adicional, como enviar una respuesta o redirigir a una página de agradecimiento
    return render(request, 'personas/contacto.html', {'form_contacto':form_contacto})
#++++++++++++++++++++++++++++++++++++++++++++++


