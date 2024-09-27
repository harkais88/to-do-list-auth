from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("create/",views.create,name="create"),
    path("delete/<int:task_id>",views.delete,name="delete"), #Delete Task
    path("update/status/<int:task_id>",views.update_status,name="status"), #Create Task
    path("display/<str:display_type>",views.display,name="display"),
]
