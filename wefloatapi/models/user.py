from django.db import models

class User(models.Model):

    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = models.TextField(default="https://i.pinimg.com/564x/42/23/7b/42237b9fd34b36ad15aca8788f6c9339.jpg")
    bio = models.CharField(max_length=150)
    uid = models.CharField(max_length=50)
