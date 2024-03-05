from django import forms
from .models import Recipe

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'preparation_steps', 'preparation_time', 'image', 'categories']



class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Обязательное поле')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']