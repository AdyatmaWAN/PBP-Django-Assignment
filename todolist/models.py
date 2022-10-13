from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class TodoListItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    description = models.TextField()
    date = models.DateField()
    is_finished = models.BooleanField(default=False)
