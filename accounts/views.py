from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.checks import messages
from django.db.models import query
from django.db.models.expressions import Ref
from django.views.generic.base import TemplateView, View
from user_panel.views import _cart_session_id
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from user_panel.models import *
from .models import Admin, RefLink
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .twilio import send_sms, gen_otp

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes




def login(request):
    user = request.user
    if user.is_authenticated:
        return redirect('user_home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
                
            try:
                user_obj = User.objects.get(username=username)
            except User.DoesNotExist:
                if user is None:
                    uname_error = 'Invalid creditials ! !'
                    context = {
                        'uname_error':uname_error,
                    }
                    return render(request, 'User/login.html', context)

            block_user_login = user_obj.is_active
            print(user_obj)

            if block_user_login == False:
                block_error = 'This user was blocked'
                context = {'block_error':block_error,}
                return render(request, 'User/login.html', context)
                
            elif user is not None:
                # This try and exception are guest cartItems merge to the user cart
                try:
                    cart = Cart.objects.get(cart_id=_cart_session_id(request))
                    exists = CartItem.objects.filter(cart=cart).exists()
                    if exists:
                        cart_item = CartItem.objects.filter(cart=cart)

                        for ct in cart_item:
                            ct.user = user
                            ct.save()
                except:
                    pass
                
                auth_login(request, user)
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
                    return redirect('user_home')
         
    return render(request, 'User/login.html')


def signup(request):
    user = request.user
    if user.is_authenticated:
        return redirect('user_home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm-password')
            if password == confirm_password:
                user = User.objects.create_user(username=username, email=email, password=password)
                auth_login(request, user)
                print("user created")
                return redirect('user_home')
            else:
                pword_error = "Password did not match ! !"
                print(pword_error)
                return render(request, 'User/signup.html', {'pword_error':pword_error})

    return render(request, 'User/signup.html')


def logout(request):
    auth_logout(request)
    request.session['admin'] = True
    return redirect('user_home')

# def admin_session(request):
#     if request.session.has_key('admin'):
#         return render(request, 'Admin/dashboard.html')
#     else:
#         return render(request, 'Admin/admin_login.html')

def admin_login(request):
    if request.session.has_key('admin'):
        # return render(request, 'Admin/dashboard.html')
        return redirect('admin_login')
    else:

        if request.method == 'POST':

            admin = Admin.objects.get(username='admin', password='admin')

            username = request.POST.get('username')
            password = request.POST.get('password')

            if username == admin.username and password == admin.password:
                print('admin logged in')
                request.session['admin'] = True
                # return JsonResponse({'status': 'ok'});
                return redirect('admin_home')
            else:
                invalid_error = "Invalid creditials ! !"
                print(invalid_error)
                # return JsonResponse({'status': 'login failed'})
                # return redirect('admin_login')
                return render(request, 'Admin/admin_login.html', {'invalid_error':invalid_error})
        else:
            return render(request, 'Admin/admin_login.html')


def admin_logout(request):
    del request.session['admin']
    return redirect('admin_login')


def change_password_request_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user_email = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'change_password/change_password_request_email.html',{'error':'Email does not exists'})

        if user_email:
            uid = urlsafe_base64_encode(force_bytes(user_email.pk))
            whoisuser = user_email.id
            token = default_token_generator.make_token(user_email)

            change_password_url = "http://127.0.0.1:8000/accounts/change_password/{}" .format(whoisuser) #{}{}".format(token)
            print(str(change_password_url) + '--change_password_url------------')

            send_mail(
                'Change password',
                "Below link allow to change your password: {}" .format(change_password_url),
                'liteboook@gmail.com',
                [email],
                fail_silently=False,
            )
            return render(request, 'change_password/email_send_done.html')
    return render(request, 'change_password/change_password_request_email.html')


def change_password(request, id):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        user = User.objects.get(id=id)

        if new_password == current_password:
            return render(request, 'change_password/change_password.html', {'error1':'New password and Current password are same'})
        elif user.password == current_password:
            if new_password == confirm_new_password:
                user.password = new_password
                user.save()
                auth_logout(request)
                return redirect('login')
            else:
                return render(request, 'change_password/change_password.html', {'error2':'New password did not match'})
        else:
            return render(request, 'change_password/change_password.html', {'error3':'Current password invalid'})
            

    return render(request, 'change_password/change_password.html')

# from ePalace import settings



def login_with_otp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        mobile_no = request.POST.get('mobile-number')
        print(str(username) + str(mobile_no) + "--- username and mobile number given from html-----")
        
        otp = gen_otp()
        message = "Hi, I hope you are going well. OTP: {}" .format(otp)
        send_sms(message, mobile_no)
        print(str(message) + "--- this is sended message -----")

        return redirect('enter_otp', otp, username)

    return render(request, 'User/logn_with_otp.html')



def enter_otp(request, otp, username):
    user = User.objects.get(username=username)
    user_enter_otp = request.POST.get('otp')

    otp_str = str(otp)
    if otp_str == user_enter_otp:
        auth_login(request, user)
        return redirect('user_home')
    else:
        print('sms otp: and html typed otp are not same')

    return render(request, 'User/enter_otp.html')




def ref_link(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        ref_link_table = RefLink.objects.get(code=code)
        request.session['ref_session'] = ref_link_table.id
    except:
        pass

    print(request.session.get_expiry_age())
    return render(request, 'User/signup.html', {})


# signup
def xxxxxx(request):
    session_id = request.session.get('ref_session')
    # sesssion nil ulla user eduthu
    recommended_user = RefLink.objects.get(id=session_id)

    # ippo register cheytha user eduthu
    user = User.objects.get(id=signup_user)

    # register cheytha user nte REflink table get cheythu
    now_registered_user = RefLink.objects.get(id=user)
    now_registered_user.recommended_by = recommended_user





def signup_with_ref_code(request, ref_code):
    user = request.user
    if user.is_authenticated:
        return redirect('user_home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm-password')
            if password == confirm_password:
                user = User.objects.create_user(username=username, email=email, password=password)

                if ref_code:
                    # session_id = request.session.get('ref_session')
                    # session_id = ref_code
                    recommended_user = RefLink.objects.get(code=ref_code)
                    user = User.objects.get(username=username)

                    print(str(user) + "---------------------- user -------------;;")

                    # register cheytha user nte REflink table get cheythu
                    now_registered_user = RefLink.objects.get(user=user)
                    print("-----------    ----------- Passed away-------------------    -------------;;")
                    now_registered_user.recommended_by = recommended_user.user
                    now_registered_user.save()
                    print("--------------- recom-by keri------------------------")

                auth_login(request, user)
                print("user created")
                return redirect('user_home')
            else:
                pword_error = "Password did not match ! !"
                print(pword_error)
                return render(request, 'User/signup.html', {'pword_error':pword_error})

    return render(request, 'User/signup.html')




# def password_reset_request(request, token):
# 	if request.method == "POST":
# 		password_reset_form = PasswordResetForm(request.POST)
# 		if password_reset_form.is_valid():
# 			data = password_reset_form.cleaned_data['email']
# 			associated_users = User.objects.filter(Q(email=data))
# 			if associated_users.exists():
# 				for user in associated_users:
# 					subject = "Password Reset Requested"
# 					email_template_name = "main/password/password_reset_email.txt"
# 					c = {
# 					"email":user.email,
# 					'domain':'127.0.0.1:8000',
# 					'site_name': 'Website',
# 					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
# 					"user": user,
# 					'token': default_token_generator.make_token(user),
# 					'protocol': 'http',
# 					}
# 					email = render_to_string(email_template_name, c)
# 					try:
# 						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
# 					except BadHeaderError:
# 						return HttpResponse('Invalid header found.')
# 					return redirect ("/password_reset/done/")
# 	password_reset_form = PasswordResetForm()
# 	return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})


