from re import X
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from accounts.models import RefLink
from django.utils import timezone
from admin_panel.models import *
from admin_panel.forms import *
from django.db.models import Q
from .models import *
import razorpay
import requests
import json
from datetime import datetime, timedelta
from .forms import FilterForm


def delete_product_offer(slug):
    product = Product.objects.get(slug=slug)
    try:
        prd_offer = ProductOffer.objects.get(product=product)
        today = datetime.now() #('2018-11-10 10:55:31', '%Y-%m-%d %H:%M:%S')

        offer_period = str(prd_offer.date_period) +" "+ str(prd_offer.time_period)
        # y = str(today)

        if offer_period < str(today):
            prd_offer.delete()
            product.product_offer_price = 0
            product.save()
            return redirect('prd_detail')
    except:
        print("------------ Exception_01 worked ----------------")

def delete_category_offer(category):
    product = Product.objects.filter(category=category)
    try:
        ctg_ofr = CategoryOffer.objects.get(category=category)
        today = datetime.now() #('2018-11-10 10:55:31', '%Y-%m-%d %H:%M:%S')

        offer_period = str(ctg_ofr.date_period) +" "+ str(ctg_ofr.time_period)
        # y = str(today)

        if offer_period < str(today):
            ctg_ofr.delete()
            for prd in product:
                prd.category_offer_price = 0
                prd.save()
            return redirect('prd_detail')
    except:
        print("------------ Exception_01 worked ----------------")



def cupon_code(request):
    if request.method == 'POST':
        cupon_code = request.POST.get('cupon_code')
        print(str(cupon_code) + "--- cupon code-----")
        try:
            cupon_code_is_exists = CuponOffer.objects.get(cupon_code=cupon_code)
            print("--- Try block worked cuponcode 01--------------------")

            request.session['cupon_code'] = cupon_code
            print("---- session created -----" + str(request.session['cupon_code']))

            
            
            return redirect('check_out')
        except:
            print("--- Exception worked cuponcode 01--------------------")
            error = "Invalid cupon code !"
            return render(request, 'User/cupon_code.html', {'error':error})

        # if cupon_code_is_exists:
        # else:

    return render(request, 'User/cupon_code.html')


# def delete_cupon_code(request):
#     print("---- session deleted -----" + str(request.session['cupon_code']))
#     del request.session['cupon_code']
#     return redirect('check_out')


def home(request):
    print(request)
    product = Product.objects.all().order_by('-id')
    context = {
        'product':product,
        # 'offer_price':offer_price,
    }
    return render(request, 'User/index.html' ,context)


def category_wised_product(request):
    laptop = Category.objects.get(category="Laptop")
    mobile = Category.objects.get(category="Mobile")
    laptop_products = Product.objects.filter(category=laptop).order_by('-id')
    mobile_products = Product.objects.filter(category=mobile).order_by('-id')

    delete_category_offer(laptop.id) # Category offer delete function called
    delete_category_offer(mobile.id) # Category offer delete function called

    context = {
        'laptop_products':laptop_products,
        'mobile_products':mobile_products,
    }
    return render(request, 'User/prd_catgry_wise.html', context)



def product_detail(request, slug):
    url_slug = slug
    product_detailed = Product.objects.get(slug=url_slug)
    print(product_detailed.category)

    delete_product_offer(url_slug) # product offer delete function called
    delete_category_offer(product_detailed.category) # Category offer delete function called

    try:
        product_offer_table = ProductOffer.objects.get(product=product_detailed)
        context = {
            'product_detailed':product_detailed,
            'product_offer_table':product_offer_table,
        }
        return render(request, 'User/productdetails.html', context)
    except:
        print("---------- Exception_01 worked -----------------")

    try:
        category_offer_table = CategoryOffer.objects.get(category=product_detailed.category)
        context = {
            'product_detailed':product_detailed,
            'category_offer_table':category_offer_table,
        }
        return render(request, 'User/productdetails.html', context)
    except:
        print("---------- Exception_02 worked -----------------")

    return render(request, 'User/productdetails.html', {'product_detailed':product_detailed,})



def search(request):
    form = FilterForm(request.POST or None)

    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        ram = request.GET.get('ram')
        storage = request.GET.get('storage')
        color = request.GET.get('color')       
        search_product = Product.objects.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(category__category__icontains=keyword) | Q(brand__sub_category__icontains=keyword) | Q(selling_price__icontains=keyword) | Q(slug__icontains=keyword))

        if ram and storage and color:
            filtered_product_by_all = search_product.filter(ram=ram, storage=storage, color=color)
            count = filtered_product_by_all.count()
            list = [ram, storage, color,]
                    
            context = {
                'search_product':filtered_product_by_all,
                'count':count,
                'keyword':keyword,
                'form':form,
                'filter_item': list,
            }
            return render(request, 'User/search-product.html', context)

        elif ram:
            filtered_product_by_ram = search_product.filter(ram=ram)
            count = filtered_product_by_ram.count()
                    
            context = {
                'search_product':filtered_product_by_ram,
                'count':count,
                'keyword':keyword,
                'form':form,
                'filter_item':ram,
            }
            return render(request, 'User/search-product.html', context)
        
        elif storage:
            filtered_product_by_storage = search_product.filter(storage=storage)
            count = filtered_product_by_storage.count()
                    
            context = {
                'search_product':filtered_product_by_storage,
                'count':count,
                'keyword':keyword,
                'form':form,
                'filter_item':storage,
            }
            return render(request, 'User/search-product.html', context)

        elif color:
            filtered_product_by_color = search_product.filter(color=color)
            count = filtered_product_by_color.count()
                    
            context = {
                'search_product':filtered_product_by_color,
                'count':count,
                'keyword':keyword,
                'form':form,
                'filter_item':color,
            }
            return render(request, 'User/search-product.html', context)

        else:
            search_product = Product.objects.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(category__category__icontains=keyword) | Q(brand__sub_category__icontains=keyword) | Q(selling_price__icontains=keyword) | Q(slug__icontains=keyword))
            count = search_product.count()

            context = {
                'search_product':search_product,
                'count':count,
                'keyword':keyword,
                'form':form,
            }
            return render(request, 'User/search-product.html', context)

    return render(request, 'User/search-product.html')



# Filter data
def filter_data(request):
    print("--------------- Filter data ------------------------")

    if request.method == "GET":
        filter_ajax_data = request.body.get('filter')
        print("--------------------------------------------------")
        print(filter_ajax_data)
        print("--------------------------------------------------")
    return JsonResponse({'data':'hello'})


def _cart_session_id(request):
    cart = request.session.session_key
    print(cart)
    if not cart:
        cart = request.session.create()
    return cart



def cart(request):
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.filter(user=request.user, is_active=True).order_by('id')
            # context = {'cart':cart,}
        else:
            cart = Cart.objects.get(cart_id=_cart_session_id(request))
            cart_item = CartItem.objects.filter(cart=cart, is_active=True).order_by('id')
            # context = {'cart':cart,}
        count = cart_item.count()
        total = 0

        for crt_itm in cart_item:
            total += (crt_itm.price * crt_itm.quantity)
            # if crt_itm.product.offer_price:
            #     total += (crt_itm.product.offer_price * crt_itm.quantity)
            # else:
        
        CartItem(sub_total=total)

        context = {
            'cart_item':cart_item,
            'count':count,
            'total':total,
        }

        # return JsonResponse(context)
        return render(request, 'User/cart.html', context)

    except ObjectDoesNotExist:
        pass
        
    return render(request, 'User/cart.html')
        


def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    try:
        cart = Cart.objects.get(cart_id=_cart_session_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_session_id(request))
    cart.save()

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(user=request.user, product=product, cart=cart)
        else:
            cart_item = CartItem.objects.get(product=product, cart=cart)
           
        if product.quantity ==  cart_item.quantity:
            pass
        else:
            cart_item.quantity += 1
            cart_item.save()
            cart_item.sub_total = cart_item.quantity * cart_item.price
            cart_item.save()

    except CartItem.DoesNotExist:
        if request.user.is_authenticated:
            if product.category_offer_price > 0:
                cart_item = CartItem.objects.create(user=request.user, product=product, cart=cart, quantity=1, price=product.category_offer_price, sub_total=product.category_offer_price)
                cart_item.save()
            elif product.product_offer_price > 0:
                cart_item = CartItem.objects.create(user=request.user, product=product, cart=cart, quantity=1, price=product.product_offer_price, sub_total=product.product_offer_price)
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(user=request.user, product=product, cart=cart, quantity=1, price=product.selling_price, sub_total=product.selling_price)
                cart_item.save()
        else:
            if product.category_offer_price > 0:
                cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1, price=product.category_offer_price, sub_total=product.category_offer_price)
                cart_item.save()
            elif product.product_offer_price > 0:
                cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1, price=product.product_offer_price, sub_total=product.product_offer_price)
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1, price=product.selling_price, sub_total=product.selling_price)
                cart_item.save()

    return redirect('cart')


def add_to_cart_ajax(request):
    print("------------- still working  ---------------")
    Disquantity = request.POST.get('Disquantity')
    cartID = request.POST.get('cartID')
    current_gnd_totl = request.POST.get('current_gnd_totl')
    cart_of_cart_item = request.POST.get('cartOfCartItem')

    # print("quantiy: " + str(Disquantity) + " cartID: "+str(cartID)+" each_tl_price: "+str(each_ttl_price)+" grand_total: "+str(all_ttl_price)+"----------------")

    cart_item = CartItem.objects.get(id=cartID)
    cart_item_itarable = CartItem.objects.filter(cart=cart_of_cart_item)
    product = Product.objects.get(title=cart_item.product)
    print("cart item: "+ str(cart_item) + " | product: " + str(product))

    if Disquantity == product.quantity:
        max_error = "Product quantity reached max level."
        print(max_error)
        data = {
            'max_error':max_error,
        }
        return JsonResponse(data)
    else:
        final_qnty = int(Disquantity) + 1
        cart_item.quantity = final_qnty
        cart_item.save()

        if product.category_offer_price:
            product_total = final_qnty * product.category_offer_price
        elif product.product_offer_price:
            product_total = final_qnty * product.product_offer_price
        else:
            product_total = final_qnty * product.selling_price
            
        # cart_item.price = product_total
        cart_item.sub_total = product_total
        cart_item.save()

        total_ = 0
        for crt in cart_item_itarable:
            total_ += crt.sub_total
        # grand_total = int(current_gnd_totl) + total_

    data = {
        'success_quantity' : final_qnty,
        'total_price' : product_total,
        'grand_total' : total_,
    }
    print("------------- working add cart 02 ---------------")
    return JsonResponse(data)


def decrement_cart_quantity_ajax(request):
    pass



def item_decrement(request, id):
    product = get_object_or_404(Product, id=id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_session_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    except:
        pass

    return redirect('cart')


def remove_item(request, id):
    product = get_object_or_404(Product, id=id)

    if request.user.is_authenticated:
        try:
            cart_item = CartItem.objects.filter(product=product, user=request.user)
        except CartItem.MultipleObjectsReturned:
            pass
    else:
        cart = Cart.objects.get(cart_id=_cart_session_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)

    cart_item.delete()
    return redirect('cart')


@login_required(login_url='login')
def check_out(request):

    current_user = request.user
    display_address = Address.objects.filter(user=current_user)
    adrs_count = display_address.count()

    # try:
    #     cart_item = CartItem.objects.get(user=current_user)
    # except CartItem.MultipleObjectsReturned:
    cart_item = CartItem.objects.filter(user=current_user)
    print(str(cart_item) + '-----cart item filter')

    total = 0
    for crt_itm in cart_item:
        total += (crt_itm.price * crt_itm.quantity)

    # ----- CUPON OFFER --------------------------------------------
    if request.session.has_key('cupon_code'):
        session = request.session['cupon_code']
        cupon_code_is_exists = CuponOffer.objects.get(cupon_code=session)
        cupon_offer_total = total - cupon_code_is_exists.offer_price
        print("--Check out part clear aaan -- total: "+str(total)+" ---cuopon code from database: "+str(cupon_code_is_exists)+" ----- offer price: "+str(cupon_code_is_exists.offer_price))
    else:
        cupon_offer_total = None

    count = cart_item.count()
    if count <= 0:
        return redirect('cart')

    if request.method == "POST":
        address = request.POST.get('address')
        payment_method = request.POST.get('payment-option')

        print(str(payment_method) + '--payment_method------')
        for item in cart_item:
            ord = Order()
            ord.user = current_user

            address_id = Address.objects.get(id=address)
            ord.shipping_address = address_id

            ord.payment = payment_method
            ord.product = item.product

            if cupon_offer_total:
                ord.product_price = cupon_offer_total
            else:
                ord.product_price = item.sub_total * item.quantity

            ord.product_quantity = item.quantity

            import datetime
            today = datetime.date.today()
            ord.time_stamp = today

            print('checkout item quantity' + str(item.quantity) + '----------')
            ord.save()

            product = Product.objects.get(id=item.product.id)
            product.quantity -= item.quantity
            product.save()
        item.cart.delete()
        
        if cupon_offer_total:
            del request.session['cupon_code']
        
        if payment_method == "paypal" or payment_method == "razorpay":
            return render(request, 'User/payment.html', {'payment_method':payment_method, 'total':total})
        else:
            return redirect('order_place_animation')
        
    context = {
        'display_address':display_address,
        'adrs_count':adrs_count,
        'total':total,
        'count':count,
        'cupon_offer_total':cupon_offer_total,
    }
    return render(request, 'User/check_out.html', context)



def razorpay(request):
    if request.method == 'POST':
        amount = 50000
        order_currency = 'INR'
        # client = razorpay.Client(auth=('rzp_test_xyIR1ZE87kJDTn', 'Xf3VouA8DPFoHfQTQ3zLUIn8'))
        # payment = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture': '1'})
        # print(str(payment) + "-- razorpay payment ditails----------")
        return redirect('order_place_animation')




def paypal(request):
    body = json.loads(request.body)
    print(str(body) + ' --- body---------')

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = 5000, #body['total_amount']
        status = body['status'],
    )
    payment.save()
    print("------------- paypal data saved-----------------")
    # return render(request, 'User/order_place_animation.html')
    # return redirect('order_place_animation')
    # return JsonResponse('fine')
    print("------------- order_place_animation func wrkd ----------------")
    return super(order_place_animation(request))



def order_place_animation(request):
    return render(request, 'User/order_place_animation.html')


def order(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    ord_count = orders.count()
    context = {
        'orders':orders,
        'ord_count':ord_count,
    }
    return render(request, 'User/order.html', context)


def order_detail(request, id):
    order_prd = Order.objects.filter(id=id)
    total = 0
    for x in order_prd:
        total += x.product_price * x.product_quantity

    context = {
        'order_prd':order_prd,
        'total':total,
    }
    return render(request, 'User/order-detail.html', context)


def cancel_order(request, id):
    order = Order.objects.get(id=id)
    order.order_status = "Cancelled"
    order.save()
    return redirect('order_detail', id)
    

def profile(request, id):
    user = User.objects.get(id=id)
    
    referral_id = RefLink.objects.get(user=user)
    referral_id_itarable = RefLink.objects.filter(recommended_by=user)
    try:

        address = Address.objects.filter(user=user)
        adrs_count = address.count()
        profile = ProfileImage.objects.get(user=user)

        context = {
            'user':user,
            'profile':profile,
            'address':address,
            'adrs_count':adrs_count,
            'referral_id':referral_id,
            'referral_id_itarable':referral_id_itarable,
        }

        return render(request, 'User/profile.html', context)
    except:
        print("------- Exception worker profile_010 -----------------")
        address = Address.objects.filter(user=user)
        error = 'Image does not exist'

        context = {
            'address':address,
            'error':error,
            'referral_id':referral_id,
            'referral_id_itarable':referral_id_itarable,
        }

        return render(request, 'User/profile.html', context)




def change_profile_image(request, id):
    user = User.objects.get(id=id)

    try:
        profile = ProfileImage.objects.get(user=user)
        form = ChangeProfileImageForm(instance=profile)

        if request.method == 'POST':
            form = ChangeProfileImageForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('profile', user.pk)

    except ProfileImage.DoesNotExist:
        form = ChangeProfileImageForm(request.POST, request.FILES)

        if request.method == 'POST':
            if form.is_valid():
                image = form.cleaned_data.get('image')
                profile = ProfileImage.objects.create(user=user, image=image)
                form.save(commit=False)
                return redirect('profile', user.pk)

    return render(request, 'User/change_profile_image.html', {'form':form})



def add_address(request, id):
    form = AddAddressForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            adrs = Address()
            adrs.user = request.user
            adrs.name = form.cleaned_data.get('name')
            adrs.mobile_number = form.cleaned_data.get('mobile_number')
            adrs.pincode = form.cleaned_data.get('pincode')
            adrs.address = form.cleaned_data.get('address')
            adrs.city = form.cleaned_data.get('city')
            adrs.state = form.cleaned_data.get('state')
            adrs.landmark = form.cleaned_data.get('landmark')
            adrs.address_type = form.cleaned_data.get('address_type')
            adrs.save()

            url = request.META.get('HTTP_REFERER')
            print(str(url) + '--- url variable -------')
            try:
                query = requests.utils.urlparse(url).query
                print(str(query) + '---login query-------')
                params = dict(x.split('=') for x in query.split('&'))
                print(str(params) + '--- params-------')

                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)
            except:
                return redirect('profile', id)

    return render(request, 'User/add_address.html', {'form':form})


def edit_address(request, id):
    user = request.user
    address = Address.objects.get(id=id)
    form = AddAddressForm(instance=address)

    if request.method == 'POST':
        form = AddAddressForm(request.POST, request.FILES, instance=address)
        if form.is_valid():
            form.save()
            url = request.META.get('HTTP_REFERER')
            print(str(url) + '--- url variable -------')
            try:
                query = requests.utils.urlparse(url).query
                print(str(query) + '---login query-------')
                params = dict(x.split('=') for x in query.split('&'))
                print(str(params) + '--- params-------')

                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)
            except:
                return redirect('profile', user.id)

    return render(request, 'User/edit_address.html', {'form':form})


def delete_address(request, id):
    user = request.user
    address = Address.objects.get(id=id)
    address.delete()
    return redirect('profile', user.id)



