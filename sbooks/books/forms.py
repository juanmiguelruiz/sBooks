from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class BusquedaTituloAutor(forms.Form):
    lib = forms.CharField(label="Titulo_autor", widget=forms.TextInput)

class RatingForm(forms.Form):
    tu_puntuacion = forms.IntegerField(max_value=5)


