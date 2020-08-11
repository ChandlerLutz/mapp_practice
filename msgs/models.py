from django.db import models

class Thread(models.Model):
    pass


class Msg(models.Model):
    text = models.TextField(default='')
    thread = models.ForeignKey(Thread, default=None, on_delete=models.CASCADE)
    
