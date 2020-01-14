from django import forms

class libros_similaresForm(forms.Form):
    idLibro = forms.CharField(label="id del libro", widget=forms.TextInput, required=True)

class recomendar_libro_usuarioForm(forms.Form):
    id_usuario = forms.IntegerField(label="Id de usuario", widget=forms.TextInput, required=True)