from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def login(request):
    user = request.user
    if user.is_authenticated:
        return redirect('user_home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('user_home')
            else:
                uname_error = 'Invalid creditials ! !'
                print(uname_error)
                return render(request, 'User/login.html', {'uname_error':uname_error})

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



def admin_login(request):
    if request.session.has_key('is_value'):
        return render(request, 'Admin/dashboard.html')
        # return redirect('admin_home')

    if request.method == 'POST':
        uname = 'admin'
        pword = 'admin'

        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == uname and password == pword:
            print('admin logged in')
            request.session['is_value'] = True
            return redirect('admin_home')
        else:
            invalid_error = "Invalid creditials ! !"
            print(invalid_error)
            return redirect('admin_login')
            # return render(request, 'Admin/admin_login.html')
    else:
        return render(request, 'Admin/admin_login.html')


def admin_logout(request):
    del request.session['is_value']
    return redirect('admin_login')