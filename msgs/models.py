from django.db import models

# Create your models here.
class Msg(models.Model):
    text = models.TextField(default='')
    
