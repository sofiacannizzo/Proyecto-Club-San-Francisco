from django.urls import path
from FinalCoderApp import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('base', views.base),
    path('accounts/login', views.login_request, name="accounts/login"),
    path('logout', views.logout_request, name="logout"),
    path('register', views.register_request, name="register"),
    path('accounts/profile', editar_perfil, name="accounts/profile"),
    path('messages', foro, name="messages"),
    path('about', acerca_de_mi, name="about"),
    
    path('socios', views.socios, name="socios"),
    path('crear_socio/', views.crear_socio, name="crear_socio"),
    path('eliminar_socio/<socio_id>/', views.eliminar_socio, name="eliminar_socio"),
    path('editar_socio/<socio_id>/', views.editar_socio, name="editar_socio"),
    path('socios/list', SociosList.as_view(), name="socios_list"),
    path(r'^nuevo$', SociosCreate.as_view(), name="socios_create"),
    path(r'^editar/(?P<pk>\d+)$', SociosUpdate.as_view(), name="socios_update"),
    path(r'^eliminar/(?P<pk>\d+)$', SociosDelete.as_view(), name="socios_delete"),
    path(r'^(?P<pk>\d+)$', SociosDetail.as_view(), name="socios_detail"),
    
    path('deportes', views.deportes, name="deportes"),
    path('crear_deporte/', views.crear_deporte, name="crear_deporte"),
    path('editar_deporte/<deporte_id>/', views.editar_deporte, name="editar_deporte"),
    path('eliminar_deporte/<deporte_id>/', views.eliminar_deporte, name="eliminar_deporte"),
    path(r'^deporte/(?P<pk>\d+)$', DeporteDetail.as_view(), name="deporte_detail"),
    
    path('profesores', views.profesores, name="profesores"),
    path('crear_profesor/', views.crear_profesor, name="crear_profesor"),
    path('editar_profesor/<profesor_id>/', views.editar_profesor, name="editar_profesor"),
    path('eliminar_profesor/<profesor_id>/', views.eliminar_profesor, name="eliminar_profesor"),
    path(r'^profesor/(?P<pk>\d+)$', ProfesorDetail.as_view(), name="profesor_detail"),
    
    path('administracion', views.administracion, name="administracion"),
    path('crear_admin/', views.crear_administrador, name="crear_admin"),
    path('editar_admin/<administrador_id>/', views.editar_administrador, name="editar_admin"),
    path('eliminar_admin/<administrador_id>/', views.eliminar_administrador, name="eliminar_admin"),
    path(r'^administrador/(?P<pk>\d+)$', AdminDetail.as_view(), name="admin_detail"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)