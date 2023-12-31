from django.contrib import admin
from .models import EstadoCivil, Persona, Titular

class PersonasAdmin(admin.ModelAdmin):
    list_display=('id','nombre', 'apellido','dni','sexo','fecha_nac','created','email','foto')
    reactonly_field=('created','update')
    search_fields=('nombre','apellido','dni') #buscador
    list_filter=('sexo','created','vive') #filtro
    date_hierarchy='fecha_nac' #filtro superior por año y mes

class EstadoCivilAdmin(admin.ModelAdmin):
    list_display=('id','nombre')
    


class TitularAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'sexo')
    list_filter = ('sexo','nombre')  #filtro por sexo y nombre


#class ApellidosAdmin(admin.ModelAdmin):
    #list_filter=('apellido',) #filtro

#class CumpleaniosAdmin(admin.ModelAdmin):
    #list_filter=('fecha_nac',) #filtro
    #date_hierarchy='fecha_nac' #filtro superior por año y mes

# admin.site.register(Persona, CumpleaniosAdmin)
admin.site.register(Persona, PersonasAdmin)
admin.site.register(EstadoCivil, EstadoCivilAdmin)
admin.site.register(Titular, TitularAdmin)
# Register your models here.
