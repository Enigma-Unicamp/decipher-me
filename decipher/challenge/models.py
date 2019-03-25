import json
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings



# Our personalized decipher challenge user model. We could use the default
# Django user model, but then it wouldn't be possible to add attributes to it
class User(AbstractUser):

    # which challenges have been done
    initial_val = ['0' for i in range(settings.NUMBER_OF_CHALLENGES)]
    initial_val = json.dumps(initial_val)
    challenges_done = models.TextField(default=initial_val)

    # points that user got
    points = models.PositiveIntegerField(default=0)

    # ranking tiebreaker
    last_capture = models.DateTimeField(default=None, null=True, blank=True)



# Challenges model
class Challenge(models.Model):
    id_chall = models.PositiveIntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=200, unique=True)
    type_chall = models.CharField(max_length=20)
    file_content = models.TextField()
    description = models.TextField()
    points = models.PositiveIntegerField(default=0)
    flag = models.CharField(max_length=200)
    solved_by = models.PositiveIntegerField(default=0)
