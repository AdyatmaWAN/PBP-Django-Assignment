from django.db import models

class WatchListItem(models.Model):
    watched = models.BooleanField()
    title = models.CharField(max_length=255)
    rating = models.IntegerField()
    release_date = models.TextField()
    review = models.TextField()

# Create your models here.
