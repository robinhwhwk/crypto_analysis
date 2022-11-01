from email.policy import default
from importlib.metadata import distribution
from django.db import models

# Create your models here.
class Ratings(models.Model):
    name = models.CharField(max_length = 255, default="")
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    positive = models.IntegerField(default=0)
    negative = models.IntegerField(default=0)
    neutral = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'date'], name='unique_name_date_combination'
            )
        ]