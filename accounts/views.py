from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def login(request):
    return render(request, 'User/login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        if password == confirm_password:
            user = User.objects.create_user(username=username, email=email, password=password)
            # user.save()
            print("user created")
            return redirect('login')
        else:
            pword_error = "Password did not match ! !"
            print(pword_error)
            return render(request, 'User/signup.html', {'pword_error':pword_error})
    return render(request, 'User/signup.html')