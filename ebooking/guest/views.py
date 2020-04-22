from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def my_login(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('index')
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password'
            return render(request, 'guest/login.html', context=context)
    
    return render(request, 'guest/login.html', context=context)



def register(request):
    context = {}

    if request.method == 'POST':
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')


        try:
            user = User.objects.get(username=request.POST.get('username'))
            
        except ObjectDoesNotExist:
            user = None

        if user:
            context = {
                'error_user' : "username ซ้ำ"
            }
            return render(request, 'guest/login.html', context)

        if password == repassword:
            user = User.objects.create_user(request.POST.get('username'), request.POST.get('email'), request.POST.get('password'))
            user.first_name = request.POST.get('firstname')
            user.last_name = request.POST.get('lastname')


            print(request.POST.get('firstname'),request.POST.get('lastname'))

            
            # group = Group.objects.get(name='myUser')
            # user.groups.add(group)
            user.save()
            return redirect('my_login')
        else:
            context['error'] = 'Password ซ้ำ'
            return render(request, 'guest/login.html', context=context)
     
    return render(request, 'guest/login.html')

def my_logout(request):
    logout(request)
    return redirect('my_login')