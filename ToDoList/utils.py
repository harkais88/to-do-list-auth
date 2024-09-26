from .models import User
from authentication.utils import get_auth_from_session

def get_user_data(request):
    return User.objects.get(id = get_auth_from_session(request))