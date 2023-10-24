
from datetime import timezone
from functools import cached_property
from ckeditor.fields import RichTextField
from django.db import models



class EstadoCivil(models.Model):
    nombre=models.CharField(max_length=30)
    def __str__(self) -> str:
        return self.nombre


    class Meta:
        verbose_name='Estado Civil'
        verbose_name_plural= 'Estados Civiles'
        #ordering=('nombre')

class Persona(models.Model):
    SEXO= [('M','Masculino'),
           ('F','Femenino'),
           ('X', 'Otro')
           ]
    
    dni= models.CharField(max_length=8, verbose_name='D.N.I.', help_text='Ingrese sin puntos', blank=True, null=True) #no requerido
    nombre= models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    fecha_nac = models.DateField(max_length=6, verbose_name='Fecha de nacimiento',default='10/10/10',help_text='dia/mes/año')
    created = models.DateTimeField(auto_now_add=True) #cuando fue creado
    update = models.DateTimeField(auto_now_add=True)  #cuando fue actualizado
    sexo= models.CharField(max_length=10, choices=SEXO, default='F', null=True, blank=True)
    estado_civil= models.ForeignKey(EstadoCivil, default='1', on_delete=models.PROTECT)
    vive = models.BooleanField(default=True)
    email = models.EmailField(max_length=250,unique=True,default='nombre@hotmail.com',null=False,blank=False) #requerido
    legajo = RichTextField(default='Legajo de Persona')
    foto = models.ImageField(
        upload_to='imagenes/',  # Ruta donde se guardarán las imágenes
        verbose_name='Foto 4x4',  # Nombre descriptivo para la interfaz de administración
        default='imagenes/avatar.png'
    )


    def __str__(self):
        return f'{self.apellido},{self.nombre}, fecha Nac{self.fecha_nac}'
    
    @cached_property
    def edad(self):
        edad=0
        if self.fecha_nac:
            dias_anual=365.2425
            edad=int((timezone.now().date()-self.fecha_nac).days / dias_anual)
        return edad

    class Meta:
        verbose_name='Persona'
        verbose_name_plural= 'Personas'
        ordering=('apellido','nombre')



class Titular(models.Model):
    # Campos del modelo Titular
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])

    # Otros campos que puedes agregar según tus necesidades

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name_plural = "Titulares"


class Contacto(models.Model):
    nombre = models.CharField(max_length=100)    
    email = models.EmailField(max_length=250)
    mensaje = models.TextField(max_length=250)


# Create your models here.
