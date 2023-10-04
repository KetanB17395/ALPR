from django.db import models

# Create your models here.
class RTSPUrlModel(models.Model):
    url = models.CharField("RTSP url",max_length=255)