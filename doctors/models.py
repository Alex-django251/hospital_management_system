from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15,blank=True, null=True)
    experience = models.IntegerField( blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
    
