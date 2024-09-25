from django.urls import path
from . import views

urlpatterns = [
    path("login/",views.login,name="login"), #Login Page
    path("register/",views.register,name="register"),#Registation Page
    path("logout/",views.logout,name="logout"), #Logout
]
