from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label = 'Email',
        max_length = 200,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'rightinput', 'name': 'email'}
        )
    )
    first_name = forms.CharField(
        label = 'First Name',
        max_length = 100,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'rightinput', 'name': 'first_name'}
        )
    )
    username = forms.CharField(
        label = 'Username',
        max_length = 100,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'rightinput', 'name': 'first_name'}
        )
    )
    last_name = forms.CharField(
        label = 'Last Name',
        max_length = 100,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'rightinput', 'name': 'last_name'}
        )

    )
    password1 = forms.CharField(
        label = 'Password',
        max_length = 100,
        required = True,
        widget = forms.PasswordInput(
            attrs = {'class': 'rightinput', 'name': 'password1'}
        )
    )
    password2 = forms.CharField(
        label = 'Confirm Password',
        max_length = 100,
        required = True,
        widget = forms.PasswordInput(
            attrs = {'class': 'rightinput', 'name': 'password2'}
        )
    )


    class Meta:
        model = User
        fields = ('first_name','last_name' , 'username', 'email', 'password1', 'password2')



class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label = 'Username',
        max_length = 100,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'rightinput', 'name': 'userame'}
        )
    )
    password = forms.CharField(
        label = 'Password',
        max_length = 100,
        required = True,
        widget = forms.PasswordInput(
            attrs = {'class': 'rightinput','name': 'password'}
        )
    )
    class Meta:
        model = User
        fields = ('username', 'password')