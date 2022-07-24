from django.contrib import admin
from FinalCoderApp.models import *

# Register your models here.
class SocioAdmin(admin.ModelAdmin):
    list_display = ('apellido','email')
    search_fields = ('apellido','email')
    
class DeporteAdmin(admin.ModelAdmin):
    list_display = ('deporte','profesor')
    search_fields = ('deporte','profesor')

class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('deporte','email')
    search_fields = ('deporte','email')

class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('puesto','email')
    search_fields = ('puesto','email')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('nombre','contenido')
    search_fields = ('nombre','contenido')


admin.site.register(Socio)
admin.site.register(Deporte, DeporteAdmin)
admin.site.register(Profesor, ProfesorAdmin)
admin.site.register(Administrador, AdministradorAdmin)
admin.site.register(Avatar)
admin.site.register(Comentario)
