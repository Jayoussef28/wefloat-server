from django.db import models

class Rating(models.Model):
  
    RATING_VALUES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]
  
    value = models.CharField(max_length=10, choices=RATING_VALUES, default='1')
