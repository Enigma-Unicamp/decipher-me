from django.db import models
from django.contrib.auth.models import AbstractUser
from private_files import PrivateFileField



# Our personalized decipher challenge user model. We could use the default
# Django user model, but then it wouldn't be possible to add attributes to it
class User(AbstractUser):
    # needed to unlock challenges or each user
    level = models.PositiveIntegerField(default=0)
    # needed by the ranking module
    last_capture = models.DateTimeField(default=None, null=True, blank=True) 



# Challenges model
class Challenge(models.Model):
    id_chall     = models.PositiveIntegerField(primary_key=True, unique=True)
    title        = models.CharField(max_length=200, unique=True)
    type_chall   = models.CharField(max_length=20)
    file_content = models.TextField()
    description  = models.TextField()
    flag         = models.CharField(max_length=200)

