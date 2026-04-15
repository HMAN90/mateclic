from django import forms
from public.models import Category
from public.models import CustomUser
from public.models import Equipment
from public.models import Rent
from django.contrib.auth.forms import UserCreationForm


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ()
        