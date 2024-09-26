from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

def get_auth_from_session(request):
    return request.session['user']