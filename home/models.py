from django.db import models
from django.conf import settings

# Create your models here.
class newsletter(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.CharField(max_length=125)

    def __str__(self):
        return self.user_id.username
    
    