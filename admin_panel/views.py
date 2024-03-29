from django.core.files.base import ContentFile
from admin_panel.models import ProductOffer
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
from django.utils import timezone

from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse, response
import csv


from .render import Render
import base64



# =========== Admin Dashboard =========================
def monthly_sales_report(request):
    try:
        from_ = request.GET['from_date']
        to_ = request.GET['to_date']
        # conver_to_pdf = request.GET['conver_to_pdf']
    
        if from_ or to_:
            x = str(from_) + "-01"
            y = str(to_) + "-01"
            
            month_order = Order.objects.filter(time_stamp__range=[x, y])
            count = month_order.count()

            context = {
                'month_order':month_order,
                'count':count,
                'from':x,
                'to':y,
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
            count = year_order.count()

            context = {
                'year_order':year_order,
                'count':count,
                'from':from_,
                'to':to_,
            }
            return render(request, 'Admin/yearly_sales_report.html', context)

    except:
        message = "*choose date"
        context = {
            'message':message,
        }
        return render(request, 'Admin/yearly_sales_report.html', context)


# def admin_session(request):
#     if 'admin' not in request.session:
#         return redirect('admin_login')
        # return render(request, 'Admin/admin_login.html')

def admin_home(request):
    if 'admin' not in request.session:
        return redirect('admin_login')

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
    # else:
    #     return redirect('admin_login') # This is not working


def convert_pdf(request, from_, to_):
    month_orders = Order.objects.filter(time_stamp__range=[from_, to_])
    html_string = render_to_string('Admin/monthly_report_pdf.html', {'month_order': month_orders})
    print("----------- this way passed 01 -------------------------")

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');
    print("----------- this way passed 02 -------------------------")

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="salesReport.pdf"'
        return response
    return response

def convert_csv(request, from_, to_):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=salesReport.csv'

    writer = csv.writer(response)
    writer.writerow(["Date", "Order ID", "User", "Product", "Payment Method", "status", "Price"])
    
    month_orders = Order.objects.filter(time_stamp__range=[from_, to_])
    for mro in month_orders:
        writer.writerow([mro.time_stamp, mro.id, mro.user.username, mro.product.title, mro.payment, mro.order_status, mro.product_price])
    
    return response



# =========== Product Management =========================

def products(request):
    if 'admin' not in request.session:
        return redirect('admin_login')
    if request.session.has_key('admin'):
        products = Product.objects.all().order_by('id')
        products_js_data = json.dumps(list(Product.objects.values()))
        context = {
            'products':products,
            'products_js_data':products_js_data,
        }
        return render(request, 'Admin/product_management.html', context)
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
    category_choice_field = Category.objects.all()
    sub_category_choice_field = SubCategory.objects.all()
    if request.method == 'POST':

        if form.is_valid():
            print(form)
            title = form.cleaned_data.get('title')
            slug = form.cleaned_data.get('slug')
            category = form.cleaned_data.get('category')
            sub_category = form.cleaned_data.get('sub_category')

            image = form.cleaned_data.get('image')
            image1 = form.cleaned_data.get('image1')
            image2 = form.cleaned_data.get('image2')
            image3 = form.cleaned_data.get('image3')

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

            # format, img1 = image.split(';base64,')
            # ext = format.split('/')[-1]
            # img_data1 = ContentFile(base64.b64decode(img1), name= title + '1.' + ext)

            # format, img2 = image1.split(';base64,')
            # ext = format.split('/')[-1]
            # img_data2 = ContentFile(base64.b64decode(img1), name= title + '2.' + ext)

            # format, img3 = image2.split(';base64,')
            # ext = format.split('/')[-1]
            # img_data3 = ContentFile(base64.b64decode(img1), name= title + '3.' + ext)

            # format, img4 = image3.split(';base64,')
            # ext = format.split('/')[-1]
            # img_data4 = ContentFile(base64.b64decode(img1), name= title + '4.' + ext)

            # product = Product.objects.create(title=title, slug=slug, category=category, sub_category=sub_category, image=image, marked_price=marked_price, selling_price=selling_price, quantity=quantity, description=description, model_number=model_number, model_name=model_name, color=color, battery_backup=battery_backup, processor_brand=processor_brand, processor_name=processor_name, storage=storage, ram=ram, size=size)
            product = Product(title, slug, category, sub_category, image, image1, image2, image3, marked_price, selling_price, quantity, description, model_number, model_name, color, battery_backup, processor_brand, processor_name, storage, ram, size)
            form.save()
            return redirect('products')
    context = {
        'create_prd_form':form,
        'category_choice_field':category_choice_field,
        'sub_category_choice_field':sub_category_choice_field,
    }
    return render(request, 'Admin/create_product.html', context)


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
    if 'admin' not in request.session:
        return redirect('admin_login')

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
    if 'admin' not in request.session:
        return redirect('admin_login')

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
    if 'admin' not in request.session:
        return redirect('admin_login')

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


# =========== Offer Management =========================
def product_offer(request):
    if 'admin' not in request.session:
        return redirect('admin_login')

    product_offer = ProductOffer.objects.all()
    context = {
        'product_offer':product_offer,
    }
    return render(request, 'Admin/Offer/product_offer.html', context)

def create_product_offer(request):
    form = CreateProductOfferForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            product = form.cleaned_data.get('product')
            offer_for = form.cleaned_data.get('offer_for')
            offer_percentage = form.cleaned_data.get('offer_percentage')
            date = form.cleaned_data.get('date')
            time = form.cleaned_data.get('time')

            ProductOffer(product, offer_for, offer_percentage, date, time)
            form.save()

            # ........................ price manage ...........................
            product = Product.objects.get(title=product)
            
            percentage_price = (product.selling_price / 100) * offer_percentage
            offer_price = product.selling_price - percentage_price
            product.product_offer_price = offer_price
            product.save()

            # try:
            # except:
            #     print("------------ Exception_01 worked ----------------")

            return redirect('product_offer')
    context = {
        'form':form,
    }
    return render(request, 'Admin/Offer/create_product_offer.html', context)
    

def edit_product_offer(request, id):
    product_offer = ProductOffer.objects.get(id=id)
    form = CreateProductOfferForm(instance=product_offer)

    if request.method == 'POST':
        form = CreateProductOfferForm(request.POST, request.FILES, instance=product_offer)
        if form.is_valid():
            form.save()

            prd_offer = ProductOffer.objects.get(id=id)
            product = Product.objects.get(title=prd_offer.product)
            percentage_price = (product.selling_price / 100) * prd_offer.offer_percentage
            offer_price = product.selling_price - percentage_price
            product.product_offer_price = offer_price
            product.save()

            return redirect('product_offer')
    return render(request, 'Admin/Offer/edit_product_offer.html', {'form':form})
    

def delete_product_offer(request, id):
    prd_ofr_del = ProductOffer.objects.get(id=id)
    prd_ofr_del.delete()
    return redirect('product_offer')
    

# .......................................................................

def category_offer(request):
    if 'admin' not in request.session:
        return redirect('admin_login')

    ctg_offer = CategoryOffer.objects.all()
    return render(request, 'Admin/Offer/category_offer.html', {'ctg_offer':ctg_offer})

def create_category_offer(request):
    form = CategoryOfferForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            category = form.cleaned_data.get('category')
            offer_for = form.cleaned_data.get('offer_for')
            offer_percentage = form.cleaned_data.get('offer_percentage')
            date = form.cleaned_data.get('date')
            time = form.cleaned_data.get('time')

            ProductOffer(category, offer_for, offer_percentage, date, time)
            form.save()

            # # .....................  price manage  ..............................
            all_prd_by_ctg = Product.objects.filter(category=category)

            for product in all_prd_by_ctg:
                percentage_price = (product.selling_price / 100) * offer_percentage
                offer_price = product.selling_price - percentage_price
                product.category_offer_price = offer_price
                product.save()

            return redirect('category_offer')
    context = {
        'form':form,
    }
    return render(request, 'Admin/Offer/create_category_offer.html', context)
    

def edit_category_offer(request, id):
    ctg_ofr = CategoryOffer.objects.get(id=id)
    form = CategoryOfferForm(instance=ctg_ofr)

    if request.method == 'POST':
        form = CategoryOfferForm(request.POST, request.FILES, instance=ctg_ofr)
        if form.is_valid():
            form.save()

            # -------------------- price manage ----------------------------------
            all_prd_by_ctg = Product.objects.filter(category=ctg_ofr.category)

            for product in all_prd_by_ctg:
                percentage_price = (product.selling_price / 100) * ctg_ofr.offer_percentage
                offer_price = product.selling_price - percentage_price
                product.category_offer_price = offer_price
                product.save()

            return redirect('category_offer')
    return render(request, 'Admin/Offer/edit_category_offer.html', {'form':form})

def delete_category_offer(request, id):
    del_ctg_ofr = CategoryOffer.objects.get(id=id)
    product = Product.objects.filter(category=del_ctg_ofr.category)
    for prd in product:
        prd.category_offer_price = 0
        prd.save()
    del_ctg_ofr.delete()
    return redirect('category_offer')

# .......................................................................

def cupon_offer(request):
    if 'admin' not in request.session:
        return redirect('admin_login')

    cupon_offer = CuponOffer.objects.all().order_by("id")
    context = {
        'cupon_offer':cupon_offer,
    }
    return render(request, 'Admin/Offer/cupon_offer.html', context)

def create_cupon_offer(request):
    form = CuponOfferForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            cupon_code = form.cleaned_data.get('cupon_code')
            offer_for = form.cleaned_data.get('offer_for')
            offer_price = form.cleaned_data.get('offer_price')
            date = form.cleaned_data.get('date')
            time = form.cleaned_data.get('time')

            ProductOffer(cupon_code, offer_for, offer_price, date, time)
            form.save()

            # ...................................................
            # product = Product.objects.get(title=product)
            # prd_offer = ProductOffer.objects.get(product=product)
            # percentage_price = (product.selling_price / 100) * prd_offer.offer_percentage
            # offer_price = product.selling_price - percentage_price
            # product.offer_price = offer_price
            # product.save()

            # try:
            # except:
            #     print("------------ Exception_01 worked ----------------")

            return redirect('cupon_offer')
    context = {
        'form':form,
    }
    return render(request, 'Admin/Offer/create_cupon_offer.html', context)

def edit_cupon_offer(request, id):
    cupon_offer = CuponOffer.objects.get(id=id)
    form = CuponOfferForm(instance=cupon_offer)

    if request.method == 'POST':
        form = CuponOfferForm(request.POST, request.FILES, instance=cupon_offer)
        if form.is_valid():
            form.save()

            # cpn_offer = CuponOffer.objects.get(id=id)
            # product = Product.objects.get(title=prd_offer.product)
            # percentage_price = (product.selling_price / 100) * prd_offer.offer_percentage
            # offer_price = product.selling_price - percentage_price
            # product.offer_price = offer_price
            # product.save()

            return redirect('cupon_offer')
    context = {
    'form':form,
    }
    return render(request, 'Admin/Offer/edit_cupon_offer.html', context)


def delete_cupon_offer(request, id):
    cpn_ofr_del = CuponOffer.objects.get(id=id)
    cpn_ofr_del.delete()
    return redirect('cupon_offer')

