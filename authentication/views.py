from django.shortcuts import render,redirect
from django.urls import reverse
from .models import User
from .utils import make_password,check_password

def login(request):
    """Login Method"""
    
    if 'user' in request.session:
        return redirect(reverse('index'))
    
    context = {}
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        try:
            user = User.objects.get(email = email, is_active = True)
            if check_password(password,user.password):
                request.session['user'] = user.id
                return redirect(reverse('index'))
            else:
                context['login_error'] = "Error Occured"
        except:
            context['login_error'] = "Error Occured"
    return render(request,'login.html',context)

def register(request):
    if 'user' in request.session:
        return redirect(reverse('index'))

    context = {}
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        new_user = User.objects.filter(email=email)
        if new_user.count() == 0:
            User(first_name=first_name,last_name=last_name,email=email,password=make_password(password)).save()
            return redirect('login')
        else:
            context['error'] = 'User already exists'
    return render(request,'register.html',context)
    
def logout(request):
    try:
        del request.session['user']
        return redirect('login')
    except Exception as e:
        print(e)
    return redirect('index')