from django.db import models

class notename(models.Model):
    name=models.CharField(max_length=255)
    date=models.DateField()

class folders(models.Model):
    name=models.CharField(max_length=255)
    files=models.CharField(max_length=255)