"""
Definition of models.
"""

from django.db import models

class InputImages(models.Model):
    set_name = models.CharField(max_length=200)
    image_1 = models.ImageField()
    image_2 = models.ImageField()


