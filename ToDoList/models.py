from django.db import models

    
class User(models.Model):
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=False)
    password = models.CharField(max_length=255,null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} Email: {self.email} Status: {self.is_active} Created At: {self.date_joined}"

class Task(models.Model):
    name = models.CharField(max_length=150)
    status_choices = [
        ("pending","pending"),
        ("complete","complete"),
    ]
    status = models.CharField(max_length=20,choices=status_choices,default="pending")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return f"Status of Task {self.name}: {self.status}"

    