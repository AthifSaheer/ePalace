from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
# from admin_panel.views import block_user


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
                auth_login(request, user)
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
    request.session['is_value'] = True
    return redirect('user_home')

def admin_session(request):
    if request.session.has_key('is_value'):
        return render(request, 'Admin/dashboard.html')
        # return redirect('admin_home')
    else:
        return redirect('admin_login')

def admin_login(request):
    admin_session(request) 

    if request.method == 'POST':
        uname = 'admin'
        pword = 'admin'

        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == uname and password == pword:
            print('admin logged in')
            request.session['is_value'] = True
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
    del request.session['is_value']
    return redirect('admin_login')