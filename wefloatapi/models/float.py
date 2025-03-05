from django.db import models
from .user import User
from .rating import Rating
from .difficulty import Difficulty

class Float(models.Model):

    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    description = models.CharField(max_length=500)
    distance = models.CharField(max_length=10) 
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE,null=False)
    image = models.TextField(default="https://i.pinimg.com/564x/42/23/7b/42237b9fd34b36ad15aca8788f6c9339.jpg")
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, null=False)
    created_on = models.DateField(auto_now_add=True)
    
