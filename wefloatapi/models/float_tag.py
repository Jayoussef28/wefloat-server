from django.db import models
from .float import Float
from .tag import Tag


class FloatTag(models.Model):
  
    float = models.ForeignKey(Float, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
