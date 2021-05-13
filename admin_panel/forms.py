from user_panel.models import *
from django import forms
from colorfield.fields import ColorField


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # fields = ['title', 'slug', 'category', 'sub_category', 'image', 'marked_price']
        fields = ('__all__')
        widgets = {
            # 'color': forms.ClorField(attrs={'type': 'color'}),
        }

class CreateCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('__all__')

class CreateSubCategory(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ('__all__')

class ChangeProfileImageForm(forms.ModelForm):
    class Meta:
        model = ProfileImage
        fields = ['image',]

class OrderStatusChangeForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ("order_status",)


class AddAddressForm(forms.ModelForm):
    
    class Meta:
        model = Address
        fields = ('name', 'mobile_number', 'pincode', 'address', 'city', 'state', 'landmark', 'address_type')
