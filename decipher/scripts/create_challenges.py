import os
import csv
from challenge.models import Challenge
from hashlib import sha256

# all challenges directories
base_path = "challenge/static/challenges_files/"

# settings file path
settings_path = "scripts/settings.csv"

# open settings file
with open(settings_path, 'r') as settings_file:

    reader = csv.reader(settings_file)

    # for each challenge...
    id_challenge = 0
    for settings in reader:

        # ... get challenge settings
        challenge_title = settings[0]
        challenge_type  = settings[1]
        challenge_flag  = settings[2]
        challenge_description = settings[3]

        # get the content path (image, download, link or page)
        content_name = os.listdir(base_path + challenge_title)
        content_path = "challenges_files/" + challenge_title + "/" + content_name[0]

        # and create the challenge object
        Challenge.objects.create(
            id_chall = id_challenge,
            type_chall = challenge_type,
            title = challenge_title,
            description = challenge_description,
            file_content = content_path,
            flag = sha256(challenge_flag.encode('utf-8')).hexdigest(),
            )

        id_challenge += 1

