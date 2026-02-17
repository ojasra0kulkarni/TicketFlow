from django.db import models  
class Data(models.Model):
  Status = models.CharField(max_length=100)
  Subject = models.CharField(max_length=200)
  Name = models.CharField(max_length=100)
  Category = models.CharField(max_length=100)
  SLA =models.TimeField()
  Date_Update =models.TimeField()

# Create your models here.
