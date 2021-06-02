from .models import Product
from django import forms


class FilterForm(forms.ModelForm):
     class Meta:
        model = Product
        fields = ['ram', 'storage', 'color']