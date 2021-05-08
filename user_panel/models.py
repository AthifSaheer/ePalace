from colorfield.fields import ColorField
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