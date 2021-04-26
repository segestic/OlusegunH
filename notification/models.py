from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Notification(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    message = models.TextField(max_length=100)