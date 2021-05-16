from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.models import Session
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from admin_panel.forms import *
from django.db.models import Q
from .models import *



def home(request):
    print(request)
    product = Product.objects.all().order_by('-id')
    return render(request, 'User/index.html' ,{'product':product})


def search(request):
    if request.method == 'GET':
        keyword = request.GET['keyword']
        search_product = Product.objects.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(category__category__icontains=keyword) | Q(brand__sub_category__icontains=keyword) | Q(selling_price__icontains=keyword) | Q(slug__icontains=keyword))
        count = search_product.count()
        print(str(search_product) + '====== search products =======')

        product = Product.objects.all()
        # print(str(product.ram) + '--ram ------------')

        context = {
            'search_product':search_product,
            'count':count,
            'product':product,
        }

        return render(request, 'User/search-product.html', context)
    
    return render(request, 'User/search-product.html')

# Filter data
def filter_data(request):
    return JsonResponse({'data':'hello'})



def product_detail(request, slug):
    url_slug = slug
    product_detailed = Product.objects.filter(slug=url_slug)
    return render(request, 'User/productdetails.html' ,{'product_detailed':product_detailed})


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

    except CartItem.DoesNotExist:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.create(user=request.user, product=product, cart=cart, quantity=1, price=product.selling_price, sub_total=product.selling_price)
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1, price=product.selling_price, sub_total=product.selling_price)
            cart_item.save()

    return redirect('cart')



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

    count = CartItem.objects.all().count()
    if count <= 0:
        return redirect('cart')

    if request.method == "POST":
        address = request.POST.get('address')
        payment = request.POST.get('payment-option')

        print(str(payment) + '--Payment method------')
        for item in cart_item:
            ord = Order()
            ord.user = current_user

            address_id = Address.objects.get(id=address)
            ord.shipping_address = address_id

            ord.payment = payment
            ord.product = item.product

            ord.product_price = item.sub_total
            ord.product_quantity = item.quantity
            print('checkout item quantity' + str(item.quantity) + '----------')
            ord.save()

            product = Product.objects.get(id=item.product.id)
            product.quantity -= item.quantity
            product.save()

            if payment == "paypal":
                return redirect('orders')

        item.cart.delete()

        return redirect('order_place_animation')

    return render(request, 'User/check_out.html', {'display_address':display_address, 'adrs_count':adrs_count})


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
    try:
        address = Address.objects.filter(user=user)
        adrs_count = address.count()
        print(adrs_count)
        profile = ProfileImage.objects.get(user=user)

        context = {
            'profile':profile,
            'address':address,
            'adrs_count':adrs_count,
        }

        return render(request, 'User/profile.html', context)
    except ProfileImage.DoesNotExist:
        address = Address.objects.filter(user=user)
        error = 'Image does not exist'

        context = {
            'address':address,
            'error':error,
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
            return redirect('profile', user.id)

    return render(request, 'User/edit_address.html', {'form':form})


def delete_address(request, id):
    user = request.user
    address = Address.objects.get(id=id)
    address.delete()
    return redirect('profile', user.id)

