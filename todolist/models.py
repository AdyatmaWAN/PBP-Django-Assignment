from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class TodoListItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    is_finished = models.BooleanField(default=False)
