from django.db import models

# Create your models here.

class GlucoseLevel(models.Model):
    user_id = models.CharField(max_length=256)
    device = models.CharField(max_length=256)
    serial_number = models.CharField(max_length=256)
    recording_type = models.SmallIntegerField()
    value = models.IntegerField()
    timestamp = models.DateTimeField()
        
    def __str__(self):
        return f"{self.user_id} - {self.value}"

