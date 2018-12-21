from django.db import models
from django.contrib.auth.models import AbstractUser


# Our personalized decipher challenge user model. We could use the default
# Django user model, but then it wouldn't be possible to add attributes to it
class User(AbstractUser):
    pass
