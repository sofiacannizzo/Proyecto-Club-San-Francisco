from concurrent.futures import ProcessPoolExecutor
from xml.sax.handler import property_declaration_handler
from django.db.models import Q
from django.shortcuts import redirect, render
from django.http import HttpResponse
from FinalCoderApp.models import *
from django.template import Template, Context
from .forms import *
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View
from django.contrib import messages

# Create your views here.
def acerca_de_mi(request):
    print(acerca_de_mi)
    return render(request, "FinalCoderApp/acerca_de_mi.html", {})

def foro(request):
    comentarios = Comentario.objects.all()
    template_name = 'FinalCoderApp/foro.html'
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():

            data = comment_form.cleaned_data
            #new_comment = Comentario(contenido=data["contenido"])
            new_comment = Comentario.objects.create(autor = request.user, contenido = data["contenido"])
            new_comment.save()
            messages.success(request, "Comentario publicado correctamente.")
    else:
        comment_form = CommentForm()
    return render(request, template_name, {'comments': comentarios,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

def inicio(request):
    inicio = Inicio.objects.all()
    print(inicio)
    return render(request, "FinalCoderApp/index.html", {"inicio": inicio}) 


def base(request):
    return render(request, "FinalCoderApp/base.html", {})

def login_request(request):
    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("inicio")
                
            else:
                return redirect("accounts/login")
        else:
            return redirect("accounts/login")
    
    form = AuthenticationForm()

    return render(request,"FinalCoderApp/login.html",{"form":form})

def register_request(request):

    if request.method == "POST":
        
        # form = UserCreationForm(request.POST)
        form = UserRegisterForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1') # es la primer contraseña, no la confirmacion

            form.save() # registramos el usuario
            # iniciamos la sesion
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("inicio")
            else:
                return redirect("login")

        return render(request,"FinalCoderApp/register.html",{"form":form})

    # form = UserCreationForm()
    form = UserRegisterForm()

    return render(request,"FinalCoderApp/register.html",{"form":form})

def logout_request(request):
    logout(request)
    messages.success(request, "Sesion cerrada.")
    return render(request, "FinalCoderApp/index.html", {"inicio": inicio})


@login_required
def editar_perfil(request):
    user = request.user # usuario con el que estamos loggueados
    try:
        avatar = Avatar.objects.get(usuario=user)
    except:
        avatar = Avatar(usuario=user)
        avatar.save()

    if request.method == "POST":
        
        form = UserEditForm2(request.POST, request.FILES) # cargamos datos llenados

        if form.is_valid():

            info = form.cleaned_data
            user.email = info["email"]
            user.first_name = info["first_name"]
            user.last_name = info["last_name"]

            user.save()

            if info['imagen'] != None:
                avatar.imagen = info['imagen']
                avatar.save()

            return redirect("inicio")

        else:
            print(form.errors)
            return render(request, "editar_perfil.html", {"form":form})

    else:
        form = UserEditForm2(initial={"email":user.email, "first_name":user.first_name, "last_name":user.last_name, "imagen":avatar.imagen})

    return render(request,"editar_perfil.html",{"form":form})


        



@login_required
def socios(request):
    if request.method == "POST":
        search = request.POST["search"]
        if search != "":
            socios = Socio.objects.filter( Q(apellido__icontains=search) | Q(deportes__icontains=search) ).values()
            return render(request, "FinalCoderApp/socios.html",{"socios":socios, "search":True, "busqueda":search})
        
    socios = Socio.objects.all()
    print(socios)
    return render(request, "FinalCoderApp/socios.html", {"socios": socios})

@staff_member_required
def crear_socio(request):
    if request.method == "POST":
        formulario = NuevoSocio(request.POST)
        print(formulario)

        if formulario.is_valid:
            info = formulario.cleaned_data
            socios = Socio(nombre=info["nombre"],apellido=info["apellido"],deportes=info["deportes"],edad=info["edad"],email=info["email"])
            socios.save()
            messages.success(request, "Socio creado correctamente.")
            return redirect("socios")

    else:
        formulario = NuevoSocio()
        return render(request,"FinalCoderApp/socio_form.html",{"form":formulario})

@staff_member_required
def eliminar_socio(request, socio_id):
    socio = Socio.objects.get(id=socio_id)
    
    if request.method=="POST":
        socio.delete()
        messages.success(request, "Socio eliminado correctamente.")
        return redirect("socios")
    
    context = {
        "socio": socio
    }
    #socio.delete()
    return render(request, "socio_confirm_delete.html", context)

@staff_member_required
def editar_socio(request, socio_id):
    socio = Socio.objects.get(id=socio_id)

    if request.method == "POST":

        formulario = NuevoSocio(request.POST)

        if formulario.is_valid():
            
            info_socio = formulario.cleaned_data
            
            socio.nombre = info_socio["nombre"]
            socio.apellido = info_socio["apellido"]
            socio.edad = info_socio["edad"]
            socio.deportes = info_socio["deportes"]
            socio.email = info_socio["email"]
            socio.save()
            messages.success(request, "Socio editado correctamente.")
            return redirect("socios")

    formulario = NuevoSocio(initial={"nombre":socio.nombre, "apellido":socio.apellido, "edad": socio.edad, "deportes": socio.deportes, "email": socio.email})
    return render(request,"FinalCoderApp/socio_form.html",{"form":formulario})


@staff_member_required
def eliminar_profesor(request, profesor_id):
    profesor = Profesor.objects.get(id=profesor_id)
    if request.method=="POST":
        profesor.delete()
        messages.success(request, "Profesor eliminado correctamente.")
        return redirect("profesores")
    context = {
        "profesor": profesor
    }
    return render(request, "profesor_confirm_delete.html", context)

@staff_member_required
def editar_profesor(request, profesor_id):
    profesor = Profesor.objects.get(id=profesor_id)

    if request.method == "POST":

        formulario = NuevoProfesor(request.POST)

        if formulario.is_valid():
            
            info_profe = formulario.cleaned_data
            
            profesor.nombre = info_profe["nombre"]
            profesor.apellido = info_profe["apellido"]
            profesor.deporte = info_profe["deporte"]
            profesor.email = info_profe["email"]
            profesor.save()
            messages.success(request, "Profesor editado correctamente.")
            return redirect("profesores")

    formulario = NuevoProfesor(initial={"nombre":profesor.nombre, "apellido":profesor.apellido, "deporte": profesor.deporte, "email": profesor.email})
    return render(request,"FinalCoderApp/profesor_form.html",{"form":formulario})

#@login_required
def profesores(request):
    if request.method == "POST":
        search = request.POST["search"]
        if search != "":
            profesores = Profesor.objects.filter( Q(apellido__icontains=search) | Q(deporte__icontains=search) ).values()
            return render(request, "FinalCoderApp/profesores.html",{"profesores":profesores, "search":True, "busqueda":search})
        
    profesores = Profesor.objects.all()
    print(profesores)
    return render(request,"FinalCoderApp/profesores.html" , {"profesores": profesores})

@staff_member_required
def crear_profesor(request):
    if request.method == "POST":
        formulario = NuevoProfesor(request.POST)
        print(formulario)

        if formulario.is_valid:
            info = formulario.cleaned_data
            profesor = Profesor(nombre=info["nombre"],apellido=info["apellido"],deporte=info["deporte"],email=info["email"])
            profesor.save()
            messages.success(request, "Profesor creado correctamente.")
            return redirect("profesores")

    else:
        formulario = NuevoProfesor()
        return render(request,"FinalCoderApp/profesor_form.html",{"form":formulario})



def deportes(request):
    if request.method == "POST":
        search = request.POST["search"]
        if search != "":
            deportes = Deporte.objects.filter( Q(profesor__icontains=search) | Q(deporte__icontains=search) ).values()
            return render(request, "FinalCoderApp/deportes.html",{"deportes":deportes, "search":True, "busqueda":search})
        
    deportes = Deporte.objects.all()
    print(deportes)
    return render(request, "FinalCoderApp/deportes.html", {"deportes": deportes})

@staff_member_required
def crear_deporte(request):
    if request.method == "POST":
        formulario = NuevoDeporte(request.POST)
        print(formulario)

        if formulario.is_valid:
            info = formulario.cleaned_data
            deporte = Deporte(deporte=info["deporte"],profesor=info["profesor"],horario=info["horario"])
            deporte.save()
            messages.success(request, "Deporte creado correctamente.")
            return redirect("deportes")

    else:
        formulario = NuevoDeporte()
        return render(request,"FinalCoderApp/deporte_form.html",{"form":formulario})

@staff_member_required
def eliminar_deporte(request, deporte_id):
    deporte = Deporte.objects.get(id=deporte_id)
    if request.method=="POST":
        deporte.delete()
        messages.success(request, "Deporte eliminado correctamente.")
        return redirect("deportes")
    context = {
        "deporte": deporte
    }
    return render(request, "deporte_confirm_delete.html", context)

@staff_member_required
def editar_deporte(request, deporte_id):
    deporte = Deporte.objects.get(id=deporte_id)

    if request.method == "POST":

        formulario = NuevoDeporte(request.POST)

        if formulario.is_valid():
            
            info_deporte = formulario.cleaned_data
            
            deporte.deporte = info_deporte["deporte"]
            deporte.profesor = info_deporte["profesor"]
            deporte.horario = info_deporte["horario"]
            deporte.save()
            messages.success(request, "Deporte editado correctamente.")
            return redirect("deportes")

    formulario = NuevoDeporte(initial={"deporte":deporte.deporte, "profesor":deporte.profesor, "horario": deporte.horario})
    return render(request,"FinalCoderApp/deporte_form.html",{"form":formulario})


@login_required
def administracion(request):
    if request.method == "POST":
        search = request.POST["search"]
        if search != "":
            administracion = Administrador.objects.filter( Q(puesto__icontains=search) | Q(apellido__icontains=search) ).values()
            return render(request, "FinalCoderApp/administracion.html",{"administracion":administracion, "search":True, "busqueda":search})
    administracion = Administrador.objects.all()
    print(administracion)
    return render(request, "FinalCoderApp/administracion.html", {"administracion": administracion})   

@staff_member_required
def crear_administrador(request):
    if request.method == "POST":
        formulario = NuevoAdministrador(request.POST)
        print(formulario)

        if formulario.is_valid:
            info = formulario.cleaned_data
            administracion = Administrador(puesto=info["puesto"],nombre=info["nombre"],apellido=info["apellido"],email=info["email"])
            administracion.save()
            messages.success(request, "Administrador creado correctamente.")
            return redirect("administracion")

    else:
        formulario = NuevoAdministrador()
        return render(request,"FinalCoderApp/admin_form.html",{"form":formulario})

@staff_member_required
def eliminar_administrador(request, administrador_id):
    administrador = Administrador.objects.get(id=administrador_id)
    if request.method=="POST":
        administrador.delete()
        messages.success(request, "Administrador eliminado correctamente.")
        return redirect("administracion")
    context = {
        "administrador": administrador
    }
    return render(request, "admin_confirm_delete.html", context)

@staff_member_required
def editar_administrador(request, administrador_id):
    
    administracion = Administrador.objects.get(id=administrador_id)

    if request.method == "POST":

        formulario = NuevoAdministrador(request.POST)

        if formulario.is_valid():
            
            info_admin = formulario.cleaned_data
            
            administracion.puesto = info_admin["puesto"]
            administracion.nombre = info_admin["nombre"]
            administracion.apellido = info_admin["apellido"]
            administracion.email = info_admin["email"]
            administracion.save()
            messages.success(request, "Administrador editado correctamente.")
            return redirect("administracion")

    formulario = NuevoAdministrador(initial={"puesto":administracion.puesto, "nombre":administracion.nombre, "apellido": administracion.apellido, "email":administracion.email})
    return render(request,"FinalCoderApp/admin_form.html",{"form":formulario})


class SociosList(LoginRequiredMixin, ListView):
    model = Socio
    template_name = "FinalCoderApp/socios_list.html"

class SociosDetail(DetailView):
    model = Socio
    template_name = "FinalCoderApp/socios_detail.html"
    
class AdminDetail(DetailView):
    model = Administrador
    template_name = "FinalCoderApp/admin_detail.html"
    
class DeporteDetail(DetailView):
    model = Deporte
    template_name = "FinalCoderApp/deporte_detail.html"
    
class ProfesorDetail(DetailView):
    model = Profesor
    template_name = "FinalCoderApp/profe_detail.html"
    
class SociosCreate(CreateView):
    model = Socio
    success_url = "/FinalCoderApp/socios/list"
    fields = ["nombre", "apellido", "edad", "deportes", "email"]

class SociosUpdate(UpdateView):
    model = Socio
    success_url = "/FinalCoderApp/socios/list"
    fields = ["nombre", "apellido", "edad", "deportes", "email"]

class SociosDelete(DeleteView):
    model = Socio
    success_url = "/FinalCoderApp/socios/list"