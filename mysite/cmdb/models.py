from django.db import models

# Create your models here.


class NBAnews(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=36, null=True)
    pubtime = models.CharField(max_length=36, null=True)
    link = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    keywords = models.CharField(max_length=200, null=True)

