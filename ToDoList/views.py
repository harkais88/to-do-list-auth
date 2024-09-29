from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Task
from .utils import get_user_data,parse_time,set_overdue
from datetime import timedelta
from django.utils import timezone

def index(request):
    """Controller for To Do List main page"""

    if 'user' not in request.session:
        return redirect(reverse('login'))

    config = {}
    user_data = get_user_data(request)
    config['user'] = f"{user_data.first_name} {user_data.last_name}"

    # Check if tasks are overdue whenever we enter site     
    set_overdue(user_data)

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
                task = Task(name = name,user_id = id,time = timedelta(hours = hours, minutes = minutes, seconds = seconds, microseconds=0))
                task.save(set_updated_at=True)
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
        task.save(set_updated_at=True)
        request.session['update_status_status'] = f"Task {task.name} updated successfully"
    return redirect('index')

def update_name(request,task_id):
    """Updates Task Name and/or Duration in To Do List"""

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
                task.time = timedelta(hours=hours,minutes=minutes,seconds=seconds, microseconds=0)

                task.save(set_updated_at=True)
                request.session['update_name_status'] = f"Task Successfully Updated"
                return redirect('index')
            else:
                config['update_name_error'] = f"Please Enter Valid Task Name"
        except Task.DoesNotExist:
            config['update_name_error'] = f"Task ID {task_id} does not exist"
    return render(request,"update_task.html",config)
    
def display(request, display_type):
    """Controller for the Display Tabs"""

    config = {}
    user_data = get_user_data(request)

    set_overdue(user_data) # Check for overdue tasks

    tasks = Task.objects.filter(user_id = user_data, status = display_type)

    config['display_type'] = "Completed" if display_type == "complete" else "Active" if display_type == "pending" else "Overdue"
    config['user'] = f"{user_data.first_name} {user_data.last_name}"
    config['tasks'] = tasks
    
    return render(request,"display.html",config)