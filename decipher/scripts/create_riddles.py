from hashlib import sha256
import shutil
import uuid
import csv
import os

from challenge.models import Riddle


Riddle.objects.create(
   id_riddle = 0,
   title = "First Riddle",
   description = "riddle description",
   hint = "riddle hint",
   flag = sha256("riddle_flag".encode('utf-8')).hexdigest(),
   visible = True
)

Riddle.objects.create(
   id_riddle = 1,
   title = "Second Riddle",
   description = "riddle description",
   hint = "riddle hint",
   flag = sha256("riddle_flag".encode('utf-8')).hexdigest(),
   visible = False
)

Riddle.objects.create(
   id_riddle = 2,
   title = "Third Riddle",
   description = "riddle description",
   hint = "riddle hint",
   flag = sha256("riddle_flag".encode('utf-8')).hexdigest(),
   visible = True
)
