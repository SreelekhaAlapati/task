from django.db import models

# Create your models here.
class Ipdetails(models.Model):
    ip=models.TextField()
    status=models.TextField()