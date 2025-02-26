from django.db import models

class Difficulty(models.Model):
  
    DIFFICULTY_CHOICES = [
        ('1', 'Easy'),
        ('2', 'Moderate'),
        ('3', 'Hard'),
        ('4', 'Extreme'),
    ]
  
    name = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
