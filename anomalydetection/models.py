from django.db import models

class Revo(models.Model):   
    Id = models.IntegerField(primary_key=True)      
    Flow_ID = models.CharField(max_length=255)
    Src_IP = models.CharField(max_length=255)
    Src_Port = models.CharField(max_length=255)
    Dst_IP = models.CharField(max_length=255)
    Dst_Port = models.CharField(max_length=255)
    Protocol = models.CharField(max_length=255)
    Timestamp = models.CharField(max_length=255)
    Classification = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "Revo"