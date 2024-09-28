from django.db import models
from authentication.models import User
from django.utils import timezone

class Task(models.Model):
    name = models.CharField(max_length=150)
    time = models.DurationField(null=True)
    status_choices = [
        ("pending","pending"),
        ("complete","complete"),
        ("overdue","overdue"),
    ]
    status = models.CharField(max_length=20,choices=status_choices,default="pending")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    updated_at = models.DateTimeField(auto_now=True)

    def is_overdue(self):
        current_time = timezone.now()
        end_time = self.updated_at + self.time
        return end_time <= current_time

    def __str__(self):
        return f"Status of Task {self.name}: {self.status} posted in email {self.user_id.email} updated at {self.updated_at} \
                Given Duration: {self.time}"

    