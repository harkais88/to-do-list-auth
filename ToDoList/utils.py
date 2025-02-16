from .models import User
from django.apps import apps
from authentication.utils import get_auth_from_session

def get_user_data(request):
    return User.objects.get(id = get_auth_from_session(request))

def parse_time(hours=0, minutes=0, seconds=0):
    hours,minutes,seconds = int(hours) if hours != "" else 0, \
                            int(minutes) if minutes != "" else 0, \
                            int(seconds) if seconds != "" else 0
    minutes += seconds // 60
    seconds = seconds % 60
    hours += minutes // 60
    minutes = minutes % 60

    return hours, minutes, seconds

def set_overdue(user_data):
    Task = apps.get_model('ToDoList', 'Task')
    tasks = Task.objects.filter(status__in=["pending","overdue"], user_id=user_data)

    for task in tasks:
        
        if task.is_overdue():
            task.status = "overdue"
            task.save(set_updated_at=False)
        else: 
            task.status = "pending"
            task.save()