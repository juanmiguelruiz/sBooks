from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import Profile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('ciudad', 'pais')


class FormSignUp(UserCreationForm):

    first_name = forms.CharField(max_length=140, required=True)
    last_name = forms.CharField(max_length=140, required=False)
    email = forms.EmailField(required=True)
    pais = forms.CharField(max_length=140, required=False)
    ciudad = forms.CharField(max_length=140, required=False)

    class Meta:
        model = User
        fields = (

            'username',
            'first_name',
            'last_name',
            'email',
            'pais',
            'ciudad',
            'password1',
            'password2',

        )
