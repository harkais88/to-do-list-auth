from django.shortcuts import render,redirect
from .models import Task, User

def index(request):
    if 'user' not in request.session:
        return redirect('login')
    
    config = {}
    # config['tasks'] = Task.objects.all()
    user_data = User.objects.get(id = request.session['user'])
    config['user'] = f"{user_data.first_name} {user_data.last_name}"
    tasks = Task.objects.filter(user_id = request.session['user'])
    config['tasks'] = tasks if tasks.count() > 0 else None
    config['create_status'] = request.session.pop('create_status',None)
    config['create_error'] = request.session.pop('create_error',None)
    config['delete_status'] = request.session.pop('delete_status',None)
    config['update_status_status'] = request.session.pop('update_status_status',None)
    config['update_status_id'] = request.session.pop('update_status_id',None)
    
    return render(request,'index.html',config)

def create(request):
    """Creates New Task in To Do List"""
    if request.method == "POST":
        id = User.objects.get(id = request.session['user'])
        name = request.POST['name']
        query = Task.objects.filter(name = name,user_id=id)
        if query.count() == 0:
            task = Task(name = name,user_id = id)
            task.save()
            request.session['create_status'] = "Task created successfully"
        else:
            request.session['create_error'] = "Task already exists"
    
    return redirect('index')

def delete(request, task_id):
    """Deletes Task in To Do List"""
    if request.method == "POST":
        id = request.session['user']
        try:
            task = Task.objects.get(id = task_id,user_id=User.id)
            task.delete()
            request.session['delete_status'] = "Task Deleted Successfully"
        except:
            request.session['delete_status'] = "Task Not Found/ Task Not Deleted Successfully"
    return redirect('index')

def update_status(request, task_id):
    """Updates Task Status in To Do List"""
    if request.method == "POST":
        id = User.objects.get(id = request.session['user'])
        task = Task.objects.get(id = task_id,user_id=id)
        task.status = request.POST['status_value']
        task.save()
        request.session['update_status_status'] = f"Task {task.name} updated successfully"
        request.session['update_status_id'] = task.id
    return redirect('index')

def login(request):
    """Login Method"""
    
    if 'user' in request.session:
        return redirect('index')
    
    context = {}
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        try:
            user = User.objects.get(email = email,password = password)
            request.session['user'] = user.id
            return redirect('index')
        except:
            context['login_error'] = "Error Occured"
    return render(request,'login.html',context)

def register(request):
    if 'user' in request.session:
        return redirect('index')

    context = {}
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        new_user = User.objects.filter(first_name=first_name,last_name=last_name,email=email)
        if new_user.count() == 0:
            User(first_name=first_name,last_name=last_name,email=email,password=password).save()
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
    