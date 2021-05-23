import re
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from user_panel.models import *
from .forms import *
import json
from json import dumps
from django.utils import timezone
from datetime import date
from django.db.models import Sum

from datetime import date, timedelta
import datetime

from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse

from django.utils import timezone
from .render import Render



# =========== Admin Dashboard =========================
def monthly_sales_report(request):
    try:
        from_ = request.GET['from_date']
        to_ = request.GET['to_date']
    
        if from_ or to_:
            x = str(from_) + "-01"
            y = str(to_) + "-01"
            
            month_order = Order.objects.filter(time_stamp__range=[x, y])

            # print(str(month_order) + "******************************************************** month order **********")

            dowload_pdf = "Dowload PDF"

            # def convert_to_pdf_01():
            #     html_string = render_to_string('Admin/monthly_report_pdf.html', {'month_order': month_order})
            #     print("----------- this way passed 01 -------------------------")

            #     html = HTML(string=html_string)
            #     html.write_pdf(target='/tmp/mypdf.pdf');
            #     print("----------- this way passed 02 -------------------------")

            #     fs = FileSystemStorage('/tmp')
            #     with fs.open('mypdf.pdf') as pdf:
            #         response = HttpResponse(pdf, content_type='application/pdf')
            #         response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
            
            # convert_to_pdf_01()
            # print(str(convert_to_pdf_01) + "----------- convert_to_pdf_01 this way passed 03 -------------------------")

            context = {
                'month_order':month_order,
                'dowload_pdf':dowload_pdf,
            }
            return render(request, 'Admin/monthly_sales_report.html', context)
    except:
        message = "*choose date"
        context = {
            'message':message,
        }
        return render(request, 'Admin/monthly_sales_report.html', context)
 


def yearly_sales_report(request):
    try:
        from_ = request.GET['from_date']
        to_ = request.GET['to_date']
        if from_ or to_:
            year_order = Order.objects.filter(time_stamp__range=[from_, to_])

            context = {
                'year_order':year_order,
            }
            return render(request, 'Admin/yearly_sales_report.html', context)

    except:
        message = "*choose date"
        context = {
            'message':message,
        }
        return render(request, 'Admin/yearly_sales_report.html', context)


def admin_home(request):
    if request.session.has_key('admin'):

        today = datetime.date.today()
        week = date.today()-timedelta(days=7)
        month = date.today()-timedelta(days=30)

        # Counts -----------------------
        user_count = User.objects.all().count()
        category_count = Category.objects.all().count()
        product_count = Product.objects.all().count()
        order_count = Order.objects.all().count()

        # DAY SALES REPORT -------------------------------------
        today_total_list = []
        prd_list_from_ord = []
        today_product_list = []
        list_ = []

        todays_order = Order.objects.values('product').annotate(Sum('product_price')).filter(time_stamp=today)

        for i in todays_order:
            for x in i.values():
                list_.append(x)
        
        for q in range(len(list_)):
            if q % 2 == 0:
                prd_list_from_ord.append(list_[q])
            else:
                today_total_list.append(list_[q])

        for prd in prd_list_from_ord:
            product = Product.objects.get(id=prd)
            prdls = product.title
            today_product_list.append(prdls)

        # Week SALES GRAPH -------------------------------------
        week_total_list = []
        week_prd_sample_list = []
        week_product_list = []
        list_01 = []
        
        week_order = Order.objects.values('product').annotate(Sum('product_price')).filter(time_stamp__range=[week, today]) #.order_by('time_stamp')
        for i in week_order:
            for x in i.values():
                list_01.append(x)

        for q in range(len(list_01)):
            if q % 2 == 0:
                week_prd_sample_list.append(list_01[q])
            else:
                week_total_list.append(list_01[q])

        for prd in week_prd_sample_list:
            product = Product.objects.get(id=prd)
            prdls = product.title
            week_product_list.append(prdls)


        # MONTH SALES GRAPH -------------------------------------
        month_total_list = []
        month_prd_sample_list = []
        month_product_list = []
        list_00 = []

        month_order = Order.objects.values('product').annotate(Sum('product_price')).filter(time_stamp__range=[month, today])
        for i in month_order:
            for x in i.values():
                list_00.append(x)

        for q in range(len(list_00)):
            if q % 2 == 0:
                month_prd_sample_list.append(list_00[q])
            else:
                month_total_list.append(list_00[q])

        for prd in month_prd_sample_list:
            product = Product.objects.get(id=prd)
            prdls = product.title
            month_product_list.append(prdls)



        context = {
            'user_count':user_count,
            'product_count':product_count,
            'order_count':order_count,
            'category_count':category_count,

            'today_total_list':today_total_list,
            'today_product_list':today_product_list,

            'week_total_list':week_total_list,
            'week_product_list':week_product_list,
            # 'year_revenue':year_total,

            'month_total_list':month_total_list,
            'month_product_list':month_product_list,
            # 'month_revenue':month_total,
        }
        return render(request, 'Admin/dashboard.html', context)
    else:
        return render(request, 'Admin/admin_login.html')


def convert_to_pdf(request):
    today = timezone.now()
    params = {
        'today': today,
        'month_order': "jk",
        'request': request
    }
    return Render.render('Admin/monthly_report_pdf.html', params)

    



# =========== Product Management =========================

def products(request):
    if request.session.has_key('admin'):
        products = Product.objects.all().order_by('id')
        return render(request, 'Admin/product_management.html', {'products':products})
    else:
        return render(request, 'Admin/admin_login.html')


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
    if request.session.has_key('admin'):
        user = User.objects.all().order_by('id')
        # user.exclude(is_staff=1)
        return render(request, 'Admin/user_management.html', {'user':user})
    else:
        return render(request, 'Admin/admin_login.html')


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
    if request.session.has_key('admin'):
        category = Category.objects.all().order_by('id')
        sub_category = SubCategory.objects.all().order_by('id')
        return render(request, 'Admin/category_management.html', {'category':category, 'sub_category':sub_category})
    else:
        return render(request, 'Admin/admin_login.html')


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
    if request.session.has_key('admin'):
        orders = Order.objects.all().order_by('-id')
        total = 0
        for x in orders:
            total += x.product_price * x.product_quantity

        context = {
            'orders':orders,
            'total':total,
        }
        return render(request, 'Admin/order_management.html', context)
    else:
        return render(request, 'Admin/admin_login.html')


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