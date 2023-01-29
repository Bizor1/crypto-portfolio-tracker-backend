from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
User = settings.AUTH_USER_MODEL
from datetime import datetime

# Create your models here.

class ExtendUser(AbstractUser):

    email = models.EmailField(blank=False, max_length=255, verbose_name="email")

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

class Transactions(models.Model):
    id=models.BigAutoField(primary_key=True)
    date_created=models.DateTimeField(datetime.now())
    asset=models.CharField(null=False,max_length=30)
    amount=models.FloatField()
    price=models.FloatField()
    transaction_type=models.CharField(null=False, max_length=4)
    user=models.ForeignKey(ExtendUser, on_delete=models.CASCADE)







    

