from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("create/",views.create,name="create"),
    path("delete/<int:task_id>",views.delete,name="delete"), #Delete Task
    path("update/status/<int:task_id>",views.update_status,name="status"), #Create Task
    path("login/",views.login,name="login"), #Login Page
    path("register/",views.register,name="register"),#Registation Page
    path("logout/",views.logout,name="logout"), #Logout
]
