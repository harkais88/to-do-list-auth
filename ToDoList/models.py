from django.db import models
from authentication.models import User
from django.utils import timezone
from .utils import parse_time

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
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, set_updated_at = False, **kwargs):
        if set_updated_at:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def is_overdue(self):
        current_time = timezone.now()
        end_time = self.updated_at + self.time
        return end_time <= current_time

    def get_pending_time(self):
        current_time = timezone.now() 
        time_passed = (self.updated_at + self.time) - current_time
        hours, minutes, seconds = parse_time(seconds=time_passed.total_seconds())

        print(f"Updated Time: {self.updated_at} Duration given: {self.time} Total: {self.updated_at + self.time} Current Time: {current_time}")
        print(f"Time Passed: {time_passed}, which means {time_passed.total_seconds()} seconds")
        print(f"Calculated: {hours} {minutes} {seconds}")
        return hours,minutes,seconds

    def __str__(self):
        return f"Status of Task {self.name}: {self.status} posted in email {self.user_id.email} updated at {self.updated_at} \
                Given Duration: {self.time}"

    