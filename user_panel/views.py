from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.models import Session
from django.http import JsonResponse, HttpResponse

from django.contrib.auth import authenticate
from django.db.models.expressions import Ref
from accounts.models import RefLink
from django.utils import timezone
from admin_panel.models import *
from admin_panel.forms import *

from django.db.models import Q
from datetime import timedelta
from .forms import FilterForm
from .models import *
from re import X

import datetime
import razorpay
import requests
import json




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
        pass

def delete_category_offer(category):
    product = Product.objects.filter(category=category)
    try:
        ctg_ofr = CategoryOffer.objects.get(category=category)
        today = datetime.now() #('2018-11-10 10:55:31', '%Y-%m-%d %H:%M:%S')

        offer_period = str(ctg_ofr.date_period) +" "+ str(ctg_ofr.time_period)

        if offer_period < str(today):
            ctg_ofr.delete()
            for prd in product:
                prd.category_offer_price = 0
                prd.save()
            return redirect('prd_detail')
    except:
        pass


def cupon_code(request):
    now = datetime.datetime.now()
    date = now.day, now.month, now.year
    time = now.hour, now.minute, now.second

    # After expiry date cupon will be delete.
    cc_del = CuponOffer.objects.all()
    for cc in cc_del:
        if str(cc.date_period) < str(date):
            if str(cc.time_period) < str(time):
                cc.delete()

    if request.method == 'POST':
        cupon_code = request.POST.get('cupon_code')

        #   CHECKING CUPON CODE IS AVAILABLE
        try:
            cupon_code_is_exists = CuponOffer.objects.get(cupon_code=cupon_code)
            if cupon_code_is_exists.is_active == True:
                error = ("Someone is using this coupon.")
                return render(request, 'User/cupon_code.html', {'error':error})
            if cupon_code_is_exists:
                cupon_code_is_exists.is_active = True
                cupon_code_is_exists.user = request.user
                cupon_code_is_exists.save()
                return redirect('check_out')

        except CuponOffer.DoesNotExist:
            # CHECKING IS SIGNUP CUPON IS AVAILABLE
            try:
                signup_cupon = SignupCupon.objects.get(cupon_code=cupon_code)
                if signup_cupon.is_active == True:
                    error = ("Someone is using this coupon.")
                    return render(request, 'User/cupon_code.html', {'error':error})
                if signup_cupon:
                    signup_cupon.is_active = True
                    signup_cupon.taken_user = request.user
                    signup_cupon.save()
                    return redirect('check_out')

            except SignupCupon.DoesNotExist:
                # CHECKING IS REFERRAL CUPON IS AVAILABLE
                try:
                    referral_cupon = ReferralCupon.objects.get(cupon_code=cupon_code)
                    if referral_cupon:
                        referral_cupon.is_active = True
                        referral_cupon.taken_user = request.user
                        referral_cupon.save()
                        return redirect('check_out')

                except ReferralCupon.DoesNotExist:
                    error = "Invalid cupon code ! !"
                    return render(request, 'User/cupon_code.html', {'error':error})

    return render(request, 'User/cupon_code.html')


def delete_cupon_code(request):
    try:
        cupn_offr = CuponOffer.objects.get(is_active=True, user=request.user)
        cupn_offr.is_active = False
        cupn_offr.user = None
        cupn_offr.save()
        return redirect('check_out')
    except CuponOffer.DoesNotExist:
        try:
            sign_cp = SignupCupon.objects.get(is_active=True, taken_user=request.user)
            sign_cp.is_active = False
            sign_cp.taken_user = None
            sign_cp.save()
            return redirect('check_out')
        except SignupCupon.DoesNotExist:
            try:
                rfr_cp = ReferralCupon.objects.get(is_active=True, taken_user=request.user)
                rfr_cp.is_active = False
                rfr_cp.taken_user = None
                rfr_cp.save()
                return redirect('check_out')
            except ReferralCupon.DoesNotExist:
                pass


def home(request):
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
    cupon_code = CuponOffer.objects.all()

    delete_product_offer(url_slug) # product offer delete function called
    delete_category_offer(product_detailed.category) # Category offer delete function called

    try:
        product_offer_table = ProductOffer.objects.get(product=product_detailed)

        context = {
            'product_detailed':product_detailed,
            'product_offer_table':product_offer_table,
            # 'cupon_code':cupon_code,
        }
        return render(request, 'User/productdetails.html', context)
    except:
        pass

    try:
        category_offer_table = CategoryOffer.objects.get(category=product_detailed.category)
        context = {
            'product_detailed':product_detailed,
            'category_offer_table':category_offer_table,
        }
        return render(request, 'User/productdetails.html', context)
    except:
        pass

    context = {
        'product_detailed':product_detailed,
        'cupon_code':cupon_code,
    }
    return render(request, 'User/productdetails.html', context)



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
    if request.method == "GET":
        filter_ajax_data = request.body.get('filter')
    return JsonRerfrl_cponse({'data':'hello'})


def _cart_session_id(request):
    cart = request.session.session_key
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
        
        CartItem(sub_total=total)

        context = {
            'cart_item':cart_item,
            'count':count,
            'total':total,
        }

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
    disply_quantity = request.POST.get('displyQuantity')
    cartProductID = request.POST.get('cartProductID')

    cart_item = CartItem.objects.get(id=cartProductID)
    cart_item_itarable = CartItem.objects.filter(cart=cart_item.cart)
    product = Product.objects.get(title=cart_item.product)

    if int(disply_quantity) == int(product.quantity):
        max_error = "Product quantity reached max level."
        data = {
            'max_error':max_error,
        }
        return JsonResponse(data)
    else:
        final_qnty = int(disply_quantity) + 1
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
        'produc_total_price' : product_total,
        'grand_total' : total_,
    }
    return JsonResponse(data)


def decrement_cart_quantity_ajax(request):
    disply_quantity = request.POST.get('displyQuantity')
    cartProductID = request.POST.get('cartProductID')

    cart_item = CartItem.objects.get(id=cartProductID)
    cart_item_itarable = CartItem.objects.filter(cart=cart_item.cart)
    product = Product.objects.get(title=cart_item.product)

    if int(disply_quantity) == 1:
        max_error = "Product quantity reached min level."
        data = {
            'max_error':max_error,
        }
        return JsonResponse(data)
    else:
        final_qnty = int(disply_quantity) - int(1)
        cart_item.quantity = final_qnty
        cart_item.save()

        if product.category_offer_price:
            product_total = final_qnty * product.category_offer_price
        elif product.product_offer_price:
            product_total = final_qnty * product.product_offer_price
        else:
            product_total = final_qnty * product.selling_price
            
        cart_item.sub_total = product_total
        cart_item.save()

        total_ = 0
        for crt in cart_item_itarable:
            total_ += crt.sub_total

    data = {
        'success_quantity' : final_qnty,
        'product_total_price' : product_total,
        'grand_total' : total_,
    }
    return JsonResponse(data)



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

    cart_item = CartItem.objects.filter(user=current_user)

    total = 0
    for crt_itm in cart_item:
        total += (crt_itm.price * crt_itm.quantity)

    # ----- CUPON OFFER --------------------------------------------
    try:
        cupon_offer = CuponOffer.objects.get(is_active=True, user=request.user)
        if cupon_offer.user == request.user:
            cupon_offer_total = total - cupon_offer.offer_price
      
    except CuponOffer.DoesNotExist:
        try:
            cupon_offer = SignupCupon.objects.get(is_active=True, taken_user=request.user)
            if cupon_offer.taken_user == request.user:
                cupon_offer_total = total - cupon_offer.offer_price
        except SignupCupon.DoesNotExist:
            try:
                cupon_offer = ReferralCupon.objects.get(is_active=True, taken_user=request.user)
                if cupon_offer.taken_user == request.user:
                    cupon_offer_total = total - cupon_offer.offer_price
            except ReferralCupon.DoesNotExist:
                cupon_offer_total = None
    

    count = cart_item.count()
    if count <= 0:
        return redirect('cart')

    if request.method == "POST":
        address = request.POST.get('address')
        payment_method = request.POST.get('payment-option')

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

            ord.save()

            product = Product.objects.get(id=item.product.id)
            product.quantity -= item.quantity
            product.save()
        item.cart.delete()
        
        if cupon_offer_total:
            cupon_offer.delete()
        
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
        return redirect('order_place_animation')




def paypal(request):
    body = json.loads(request.body)

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = 5000, #body['total_amount']
        status = body['status'],
    )
    payment.save()
    # return render(request, 'User/order_place_animation.html')
    # return redirect('order_place_animation')
    # return JsonResponse('fine')
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
    
    # PROFILE IMAGE -----------------------------
    profile_img = ProfileImage.objects.all()
    for p_img in profile_img:
        if p_img.user == request.user:
            profile_image = ProfileImage.objects.get(user=user)
            break
        else:
            profile_image = None

    # ADDRESS --------------------------------
    all_adrs = Address.objects.all()
    for add in all_adrs:
        if add.user == request.user:
            address = Address.objects.filter(user=user)
            address_count = address.count()
            break
        else:
            address = None
            address_count = 0

    # REFERRAL DETAILS ------------------------------
    referral_link = RefLink.objects.all()
    for rfr_lnk in referral_link:
        if rfr_lnk.user == request.user:
            referral_code = RefLink.objects.get(user=user)
            referral_code_itarable = RefLink.objects.filter(recommended_by=user)
            break
        else:
            referral_code_itarable = None
            referral_code = None
    
    # SIGNUP CUPON --------------------------------
    signup = SignupCupon.objects.all()
    for sc in signup:
        if sc.which_user == request.user:
            signup_cupon = SignupCupon.objects.get(which_user=request.user)
            break
        else:
            signup_cupon = None

    # REFERRAL CUPON -------------------------------------
    referral = ReferralCupon.objects.all()
    for rf in referral:
        if rf.which_user == request.user:
            referral_cupon = ReferralCupon.objects.filter(which_user=request.user)
            break
        else:
            referral_cupon = None

    context = {
        'user':user,
        'profile_image':profile_image,

        'address':address,
        'address_count':address_count,
        
        'referral_code':referral_code,
        'referral_code_itarable':referral_code_itarable,

        'signup_cupon':signup_cupon,
        'referral_cupon':referral_cupon,
    }

    return render(request, 'User/profile.html', context)
    return render(request, 'User/profile.html')




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
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))

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
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))

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



