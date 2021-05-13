from re import U
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from colorfield.fields import ColorField
from django.urls import reverse
from django.db import models


class Category(models.Model):
    category = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.category

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategory', on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.sub_category

color_choice = [
    ('#FFFF',"white"),
    ('#0000',"Black"),
]
ram_choice = [
    ('4GB',"4GB"),
    ('8GB',"8GB"),
    ('8GB',"8GB"),
]
storage_choice = [
    ("64GB","64GB"),
    ('128GB',"128GB"),
]


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, related_name='prd_catg', on_delete=models.CASCADE)
    brand = models.ForeignKey(SubCategory, related_name='prd_catg', on_delete=models.CASCADE)

    image = models.ImageField(upload_to='prd_imgs')
    more_image_one = models.ImageField(upload_to='prd_imgs')
    more_image_two = models.ImageField(upload_to='prd_imgs')
    more_image_three = models.ImageField(upload_to='prd_imgs')

    marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    guarandeed = models.BooleanField()
    description = models.TextField()
    
    model_number = models.CharField(max_length=10, null=True, blank=True)
    model_name = models.CharField(max_length=10, null=True, blank=True)
    color = ColorField(default='#FF0000')
    battery_backup = models.CharField(max_length=15, null=True, blank=True, default='Upto 3 hours')
    processor_brand = models.CharField(max_length=15, null=True, blank=True)
    processor_name = models.CharField(max_length=15, null=True, blank=True)
    storage = models.CharField(max_length=15, choices=storage_choice, null=True, blank=True)
    ram = models.CharField(max_length=15, choices=ram_choice, null=True, blank=True)
    size = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.title


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    sub_total = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def su_btotal(self):
        total = self.quantity * self.price
        return total


    def __str__(self):
        return self.product.title
      
    

class ProfileImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_imgs')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username

state = [
    ("Kerala","Kerala"),
    ('UP',"UP"),
    ('Tamilnad',"Tamilnad"),
]

address_type = [
    ("Home","Home"),
    ('Work',"Work"),
]

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    mobile_number = models.PositiveIntegerField()
    pincode = models.PositiveIntegerField()
    # email = models.CharField(max_length=250)
    address = models.CharField(max_length=245)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, choices=state)
    landmark = models.CharField(max_length=100, null=True, blank=True)
    address_type = models.CharField(max_length=5, choices=address_type)


    def __str__(self):
        return self.name +' | ' + self.user.username
    
payment = [
    ('Paypal','Paypal'),
    ('COD','COD'),
]

order_status = [
    ('Ordered','Ordered'),
    ('Packed','Packed'),
    ('Shipped','Shipped'),
    ('Delivered','Delivered'),
    ('Cancelled','Cancelled'),
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment = models.CharField(max_length=20, choices=payment)
    order_status = models.CharField(max_length=50, choices=order_status, default='Ordered')
    date = models.DateTimeField(auto_now_add=True)
   
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    product_price = models.PositiveIntegerField()
    product_quantity = models.PositiveIntegerField()

    def __str__(self):
        return 'ID: ' + str(self.id) + ' | User: ' + self.user.username + ' | Product: ' + str(self.product.title)
    