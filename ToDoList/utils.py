from .models import User
from authentication.utils import get_auth_from_session

def get_user_data(request):
    return User.objects.get(id = get_auth_from_session(request))

def parse_time(hours, minutes, seconds):
    hours,minutes,seconds = int(hours) if hours != "" else 0, \
                            int(minutes) if minutes != "" else 0, \
                            int(seconds) if seconds != "" else 0
    minutes += seconds // 60
    seconds = seconds % 60
    hours += minutes // 60
    minutes = minutes % 60

    return hours, minutes, seconds