from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("create/",views.create,name="create"), #Create Task
    path("delete/<int:task_id>",views.delete,name="delete"), #Delete Task
    path("update/status/<int:task_id>",views.update_status,name="status"), #Update Task Status
    path("update/name/<int:task_id>",views.update_name,name="name"), #Update Task Name
    path("display/<str:display_type>",views.display,name="display"),
]
