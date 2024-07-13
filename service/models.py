from django.db import models

# Create your models here.

class ServiceModels(models.Model):
    name = models.CharField(max_length=20)
    descriptions = models.TextField()
    image = models.ImageField(upload_to='service/images/')

