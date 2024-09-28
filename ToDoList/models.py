from django.db import models
from authentication.models import User

class Task(models.Model):
    name = models.CharField(max_length=150)
    time = models.TimeField(null=True)
    status_choices = [
        ("pending","pending"),
        ("complete","complete"),
        ("overdue","overdue"),
    ]
    status = models.CharField(max_length=20,choices=status_choices,default="pending")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return f"Status of Task {self.name}: {self.status} posted in email {self.user_id.email}"

    