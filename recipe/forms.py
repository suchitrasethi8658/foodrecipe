from django import forms

from .models import *


class RegisterForms(forms.ModelForm):
    class Meta:
        model=RegisterModel
        fields=("userid","firstname","lastname","password","phoneno","email","gender",)

class LoginForm(forms.Form):
    userid = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput)

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'ingredients', 'steps', 'image']
        exclude = ['author']
