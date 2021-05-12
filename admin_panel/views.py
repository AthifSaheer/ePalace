import re
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from user_panel.models import *
from .forms import *
from accounts.views import admin_session
import json


# =========== Admin Dashboard =========================

def admin_home(request):
    admin_session(request)
    return render(request, 'Admin/dashboard.html')


# =========== Product Management =========================

def products(request):
    products = Product.objects.all().order_by('id')
    return render(request, 'Admin/product_management.html', {'products':products})

def delete_product(request, id):
    prd_id = id
    product = Product.objects.filter(id=id)
    product.delete()
    return redirect('products')
    # return render()

def create_products(request):
    form = CreateProductForm(request.POST, request.FILES)
    if request.method == 'POST':

        if form.is_valid():
            print(form)
            title = form.cleaned_data.get('title')
            slug = form.cleaned_data.get('slug')
            category = form.cleaned_data.get('category')
            sub_category = form.cleaned_data.get('sub_category')
            image = form.cleaned_data.get('image')

            marked_price = form.cleaned_data['marked_price']
            selling_price = form.cleaned_data['selling_price']
            quantity = form.cleaned_data['quantity']

            description = form.cleaned_data.get('description')
            model_number = form.cleaned_data.get('model_number')
            model_name = form.cleaned_data.get('model_name')
            color = form.cleaned_data.get('color')
            battery_backup = form.cleaned_data.get('battery_backup')
            processor_brand = form.cleaned_data.get('processor_brand')
            processor_name = form.cleaned_data.get('processor_name')
            storage = form.cleaned_data.get('storage')
            ram = form.cleaned_data.get('ram')
            size = form.cleaned_data.get('size')

            # product = Product.objects.create(title=title, slug=slug, category=category, sub_category=sub_category, image=image, marked_price=marked_price, selling_price=selling_price, quantity=quantity, description=description, model_number=model_number, model_name=model_name, color=color, battery_backup=battery_backup, processor_brand=processor_brand, processor_name=processor_name, storage=storage, ram=ram, size=size)
            product = Product(title, slug, category, sub_category, image, marked_price, selling_price, quantity, description, model_number, model_name, color, battery_backup, processor_brand, processor_name, storage, ram, size)
            form.save()
            return redirect('products')
    return render(request, 'Admin/create_product.html', {'create_prd_form':form})


def edit_product(request, id):
    product = Product.objects.get(id=id)
    form = CreateProductForm(instance=product)

    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')

    return render(request, 'Admin/edit_product.html', {'form':form})


# =========== User Management =========================

def users(request):
    user = User.objects.all().order_by('id')
    # user.exclude(is_staff=1)
    return render(request, 'Admin/user_management.html', {'user':user})


def block_user(request, username):
    user = User.objects.get(username=username)
    user.is_active = False
    user.save()
    print(user)

    return redirect('users')

def un_block_user(request, id):
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    return redirect('users')

def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    print("Deleted user")
    # user.save()
    return redirect('users')


# =========== Category Management =========================

def categories(request):
    category = Category.objects.all().order_by('id')
    sub_category = SubCategory.objects.all().order_by('id')
    return render(request, 'Admin/category_management.html', {'category':category, 'sub_category':sub_category})


def create_category(request):
    form = CreateCategory(request.POST)

    if request.method == 'POST':

        if form.is_valid():
            catgry = form.cleaned_data.get('category')
            slug = form.cleaned_data['slug']
            print(slug)
            print("-----form clened_data-----" + str(form.cleaned_data))

            category = Category(catgry, slug)
            form.save()
            return redirect('categories')

    return render(request, 'Admin/create_category.html', {'form':form})

def edit_category(request, id):
    cat = Category.objects.get(id=id)
    form = CreateCategory(instance=cat)

    if request.method == 'POST':
        form = CreateCategory(request.POST, request.FILES, instance=cat)
        if form.is_valid():
            form.save()
            return redirect('categories')
    
    return render(request, 'Admin/edit_category.html', {'form':form})


def delete_category(request, id):
    del_category = Category.objects.get(id=id)
    del_category.delete()
    return redirect('categories')


def create_sub_category(request):
    form = CreateSubCategory(request.POST)

    if request.method == 'POST':

        if form.is_valid():
            sub_catgry = form.cleaned_data.get('category')
            catgry = form.cleaned_data.get('sub_category')
            slug = form.cleaned_data['slug']

            category = SubCategory(sub_catgry, catgry, slug)
            form.save()
            return redirect('categories')

    return render(request, 'Admin/create_sub_category.html', {'form':form})


def edit_sub_category(request, id):
    sub_cat = SubCategory.objects.get(id=id)
    form = CreateSubCategory(instance=sub_cat)

    if request.method == 'POST':
        form = CreateSubCategory(request.POST, request.FILES, instance=sub_cat)
        if form.is_valid():
            form.save()
            return redirect('categories')
    
    return render(request, 'Admin/edit_sub_category.html', {'form':form})


def delete_sub_category(request, id):
    del_sub_category = SubCategory.objects.get(id=id)
    del_sub_category.delete()
    return redirect('categories')


# =========== Order Management =========================

def orders(request):
    orders = Order.objects.all().order_by('-id')
    total = 0
    for x in orders:
        total += x.product_price * x.product_quantity

    context = {
        'orders':orders,
        'total':total,
    }
    return render(request, 'Admin/order_management.html', context)

def orders_status_change(request, id):
    orders = Order.objects.filter(id=id)
    total = 0
    for x in orders:
        total += x.product_price * x.product_quantity

    # =========================================================
    # form = OrderStatusChangeForm(request=POST)
    ord_sts_chng = Order.objects.get(id=id)
    form = OrderStatusChangeForm(instance=ord_sts_chng)

    if request.method == 'POST':
        form = OrderStatusChangeForm(request.POST, request.FILES, instance=ord_sts_chng)
        if form.is_valid():
            form.save()
            return redirect('orders')
    # =========================================================
    context = {
        'orders':orders,
        'total':total,
        'form':form,
    }
    return render(request, 'Admin/orders_status_change.html', context)