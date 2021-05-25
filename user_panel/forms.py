from django import forms
from .models import Product


class FilterForm(forms.ModelForm):
     class Meta:
        model = Product
        fields = ['ram', 'storage', 'color']