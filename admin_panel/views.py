from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from user_panel.models import *
from .forms import *



# =========== Admin Dashboard =========================

def admin_home(request):
    if request.session.has_key('is_value'):
        return render(request, 'Admin/dashboard.html')
        # return redirect('admin_home')
    else:
        # return render(request, 'Admin/admin_login.html')
        return redirect('admin_login')


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


def block_user(request, id):
    user = User.objects.get(id=id)
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
    category = Category.objects.all()
    sub_category = SubCategory.objects.all()
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