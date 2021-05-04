from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


def login(request):
    user = request.user
    if user.is_authenticated:
        return redirect('user_home')
    else:
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
    return redirect('user_home')

def admin_login(request):
    uname = 'admin'
    pword = 'admin'

    username = request.POST.get('username')
    password = request.POST.get('password')

    if username == uname and password == pword:
        print('admin logged in')
        return redirect('admin_home')
    else:
        invalid_error = "Invalid creditials ! !"
        print(invalid_error)
    return render(request, 'Admin/admin_login.html', {'invalid_error':invalid_error})


def admin_logout(request):
    print("admin log out")