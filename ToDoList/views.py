from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Task
from .utils import get_user_data,parse_time
from datetime import time

def index(request):
    if 'user' not in request.session:
        return redirect(reverse('login'))
    
    config = {}
    user_data = get_user_data(request)
    config['user'] = f"{user_data.first_name} {user_data.last_name}"
    tasks = Task.objects.filter(user_id = user_data)
    config['tasks'] = tasks if tasks.count() > 0 else None
    config['create_status'] = request.session.pop('create_status',None)
    config['create_error'] = request.session.pop('create_error',None)
    config['delete_status'] = request.session.pop('delete_status',None)
    config['update_status_status'] = request.session.pop('update_status_status',None)
    config['update_name_status'] = request.session.pop('update_name_status',None)
    config['update_name_error'] = request.session.pop('update_name_error',None)
    
    return render(request,'index.html',config)

def create(request):
    """Creates New Task in To Do List"""
    if request.method == "POST":
        id = get_user_data(request)
        name = request.POST['name']
        hours, minutes, seconds = parse_time(request.POST['hours'], request.POST['minutes'], request.POST['seconds'])
        if name != "": 
            query = Task.objects.filter(name = name,user_id=id)
            if query.count() == 0:
                task = Task(name = name,user_id = id,time = time(hour = hours, minute = minutes, second = seconds))
                task.save()
                request.session['create_status'] = "Task created successfully"
            else:
                request.session['create_error'] = "Task already exists"
        else:
            request.session['create_error'] = "Please enter task"

    return redirect('index')

def delete(request, task_id):
    """Deletes Task in To Do List"""
    if request.method == "POST":
        id = get_user_data(request)
        try:
            task = Task.objects.get(id = task_id,user_id=id)
            task.delete()
            request.session['delete_status'] = "Task Deleted Successfully"
        except:
            request.session['delete_status'] = "Task Not Found/ Task Not Deleted Successfully"
    return redirect('index')

def update_status(request, task_id):
    """Updates Task Status in To Do List"""
    if request.method == "POST":
        id = get_user_data(request)
        task = Task.objects.get(id = task_id,user_id=id)
        task.status = request.POST['status_value']
        task.save()
        request.session['update_status_status'] = f"Task {task.name} updated successfully"
        # request.session['update_status_id'] = task.id
    return redirect('index')

def update_name(request,task_id):
    user_data = get_user_data(request)
    task = Task.objects.get(id = task_id, user_id= user_data)
    config = {'task': task, 'user': f"{user_data.first_name} {user_data.last_name}"}
    if request.method == "POST":
        try:
            if request.POST['updated_name'] != "":
                task.name = request.POST['updated_name']
                hours,minutes,seconds = parse_time(hours = request.POST['updated_hours'],
                                       minutes = request.POST['updated_minutes'],
                                       seconds = request.POST['updated_seconds'])
                task.time = time(hour=hours,minute=minutes,second=seconds)

                task.save()
                request.session['update_name_status'] = f"Task Name Updated"
                return redirect('index')
                # config['update_name_status'] = f"Task Name Updated"
            else:
                # request.session['update_name_error'] = f"Please Enter Valid Task Name"
                config['update_name_error'] = f"Please Enter Valid Task Name"
        except Task.DoesNotExist:
            # request.session['update_name_status'] = f"Task ID {task_id} does not exist"
            config['update_name_error'] = f"Task ID {task_id} does not exist"
    # return redirect('index')
    return render(request,"update_task.html",config)
    
def display(request, display_type):
    config = {}
    user_data = get_user_data(request)
    tasks = Task.objects.filter(user_id = user_data, status = display_type)

    config['display_type'] = "Completed" if display_type == "complete" else "Active"
    config['user'] = f"{user_data.first_name} {user_data.last_name}"
    config['tasks'] = tasks
    
    return render(request,"display.html",config)