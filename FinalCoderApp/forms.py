from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Avatar, Comentario
from django.core.files import File
from django.core.files.images import get_image_dimensions

class NuevoSocio(forms.Form):
    nombre = forms.CharField(max_length=30,label="Nombre")
    apellido = forms.CharField(max_length=30,label="Apellido")
    edad = forms.IntegerField(min_value=1,label="Edad")
    deportes = forms.CharField(max_length=30,label="Deportes")
    email = forms.EmailField(label="Email")

class NuevoProfesor(forms.Form):
    nombre = forms.CharField(max_length=30,label="Nombre")   #cambiar
    apellido = forms.CharField(max_length=30,label="Apellido")
    deporte = forms.CharField(max_length=30,label="Deporte")
    email = forms.EmailField(label="Email")

class NuevoDeporte(forms.Form):
    deporte = forms.CharField(max_length=30,label="Deporte")
    profesor = forms.CharField(max_length=70,label="Profesor")
    horario = forms.CharField(label="Horario")
    
class NuevoAdministrador(forms.Form):
    puesto = forms.CharField(max_length=100,label="Puesto")
    nombre = forms.CharField(max_length=30,label="Nombre")
    apellido = forms.CharField(max_length=30,label="Apellido")
    email = forms.EmailField(label="Email")
    
class UserRegisterForm(UserCreationForm):
    
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput) # la contraseña no se vea
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    first_name = forms.CharField(label="Nombre", required=False)
    last_name = forms.CharField(label="Apellido", required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

class UserEditForm(UserCreationForm):

    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=False) # la contraseña no se vea
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput, required=False)

    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name']

        help_texts = {k:"" for k in fields}

class UserEditForm2(forms.Form):

    email = forms.EmailField(label="Email")
    imagen = forms.ImageField(label="Imagen", required=False)

    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")
        

class CommentForm(forms.Form):
    contenido = forms.CharField(label ="", widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'placeholder':'Comente aquí !',
        'rows':4,
        'cols':50
    }))
    class Meta:
        model = Comentario
        fields =['content']