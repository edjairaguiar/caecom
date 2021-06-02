from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import fields, widgets
from .models import Questao, Resposta
from django import forms
from django.db import models


class RegisterUserForm(UserCreationForm): 
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={
                'required': True,
                'placeholder': 'exemplo@discente.univasf.edu.br',
                'autofocus': True
            }),
            'username': forms.TextInput(attrs={
                'required': True,
                'placeholder': 'exemplo',
            })
        }
    
    def __init__(self, *args, **kwargs): 
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs = {'placeholder': 'senha'}
        self.fields['password2'].widget.attrs = {'placeholder': 'confirmar senha'}

class LoginForm(AuthenticationForm):
    class Meta:
        fields = '__all__'

class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = Questao
        fields = ['title', 'body', 'area']
        widgets = {
            'title': forms.TextInput(attrs={
                'autofocus': True,
                'placeholder': 'entitule a sua pergunta. evite ser ofensivo!'
            })
        }

class NewResponseForm(forms.ModelForm):
    class Meta:
        model = Resposta
        fields = ['body']

class NewReplyForm(forms.ModelForm):
    class Meta:
        model = Resposta
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'no que você está pensando?'
            })
        }