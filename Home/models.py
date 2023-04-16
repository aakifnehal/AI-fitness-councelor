from django.db import models

# Create your models here.
class userData(models.Model):
    userName=models.CharField(max_length=122)
    weight=models.IntegerField()
    hieght=models.IntegerField()
    bmi=models.FloatField()
    date=models.DateField()

