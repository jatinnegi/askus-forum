from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(label="", required=True, widget=forms.TextInput(
        attrs={
            'placeholder': 'Username Or Email',
            'class': 'form-control',
            'autocomplete': 'off',
            'id': 'username',
            'autofocus': True,
        }
    ))

    password = forms.CharField(label="", required=True, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'class': 'form-control',
            'id': 'password',
        }
    ))
    error_messages = {
        'invalid_login': _("Invalid credentials. Try again."),
        'inactive': _("This account is inactive."),
    }


class SignUpForm(UserCreationForm):
    email = forms.CharField(label="", required=True, widget=forms.TextInput(
        attrs={
            'placeholder': 'Email',
            'class': 'form-control',
            'autocomplete': 'off',
            'id': 'email',
            'autofocus': True
        }
    ))

    username = forms.CharField(label="", required=True, widget=forms.TextInput(
        attrs={
            'placeholder': 'Username',
            'class': 'form-control',
            'autocomplete': 'off',
            'id': 'username',
        }
    ))

    password1 = forms.CharField(label="", required=True, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'class': 'form-control',
            'autocomplete': 'off',
            'id': 'password1'
        }
    ))

    password2 = forms.CharField(label="", required=True, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Confirm password',
            'class': 'form-control',
            'autocomplete': 'off',
            'id': 'password2'
        }
    ))

    first_name = forms.CharField(label="", required=False, widget=forms.TextInput(
        attrs={
            'placeholder': 'First Name (Optional)',
            'class': 'form-control',
            'autocomplete': 'off',
            'id': 'first_name',
        }
    ))

    last_name = forms.CharField(label="", required=False, widget=forms.TextInput(
        attrs={
            'placeholder': 'Last Name (Optional)',
            'class': 'form-control',
            'autocomplete': 'off',
            'id': 'last_name',
        }
    ))

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', )


class AvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar',)
