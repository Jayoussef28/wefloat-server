from django.db import models
from .float import Float
from .user import User
from .rating import Rating

class Comment(models.Model):

    float = models.ForeignKey(Float, on_delete=models.CASCADE, null=False)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, null=False)
    body = models.CharField(max_length=500)
    created_on = models.DateField()
