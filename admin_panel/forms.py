from user_panel.models import *
from django import forms
from colorfield.fields import ColorField
from .models import *


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'slug', 'category', 'brand', 'image', 'more_image_one', 'more_image_two', 'more_image_three', 'marked_price', 'selling_price', 'quantity', 'guarandeed', 'description', 'model_number', 'model_name', 'color', 'battery_backup', 'processor_brand', 'processor_name', 'storage', 'ram', 'size']
 

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


# ........................ OFFER FORMS............................ ........................
class DateInput(forms.DateInput):
    input_type = 'time' 

class CreateProductOfferForm(forms.ModelForm):
    date_period = forms.DateField(
        # input_formats = ['%Y-%m-%d'],
        widget=forms.TextInput(     
            attrs={'type': 'date'} 
        )
    )
    time_period = forms.TimeField(
        widget = forms.TextInput(
            attrs={'type': 'time'},
        )
    )

    class Meta:
        model = ProductOffer
        fields = ['product', 'offer_for', 'offer_percentage','date_period', 'time_period']


class CuponOfferForm(forms.ModelForm):
    date_period = forms.DateField(
        # input_formats = ['%Y-%m-%d'],
        widget=forms.TextInput(     
            attrs={'type': 'date'} 
        )
    )
    time_period = forms.TimeField(
        widget = forms.TextInput(
            attrs={'type': 'time'},
        )
    )

    class Meta:
        model = CuponOffer
        fields = ['cupon_code', 'offer_for', 'offer_price','date_period', 'time_period']



class CategoryOfferForm(forms.ModelForm):
    date_period = forms.DateField(
        # input_formats = ['%Y-%m-%d'],
        widget=forms.TextInput(     
            attrs={'type': 'date'} 
        )
    )
    time_period = forms.TimeField(
        widget = forms.TextInput(
            attrs={'type': 'time'},
        )
    )

    class Meta:
        model = CategoryOffer
        fields = ['category', 'offer_for', 'offer_percentage','date_period', 'time_period']


