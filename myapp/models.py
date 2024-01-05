from django.db import models

# Create your models here.



class Jurnal(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    link = models.CharField(max_length=150)
    abstracturl = models.CharField(max_length=150)

    class Meta:
        db_table = "tbjurnal"