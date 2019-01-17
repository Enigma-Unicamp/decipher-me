import os
import csv
import uuid
import shutil
from challenge.models import Challenge
from hashlib import sha256


# all challenges directories
base_path = "challenge/static/challenges_files/"

# first of all, clone challenges_files directory
# from scripts folder to challenge/static folder
try:
    shutil.copytree("scripts/challenges_files", base_path)
except:
    shutil.rmtree(base_path)
    shutil.copytree("scripts/challenges_files", base_path)

# settings file path
settings_path = "scripts/settings.csv"

# open settings file
with open(settings_path, 'r') as settings_file:

    reader = csv.reader(settings_file)

    # for each challenge...
    id_challenge = 0
    unique_key = []
    for settings in reader:

        # ... get challenge settings
        challenge_title = settings[0]
        challenge_type  = settings[1]
        challenge_flag  = settings[2]
        challenge_description = settings[3]

        # generate unique key to ubfuscate challenge folder
        new_key = uuid.uuid4().hex[:25]
        while new_key in unique_key:
            new_key = uuid.uuid4().hex[:25]
        unique_key.append(new_key)

        # rename challenge folder (to ubfuscate)
        new_title = unique_key[id_challenge]
        os.makedirs(base_path + new_title, exist_ok=True)
        os.rename(base_path + challenge_title, base_path + new_title)

        # get the content path (image, download, link or page)
        content_files = os.listdir(base_path + new_title)
        if challenge_type != 'page':
            content_path = "challenges_files/" + new_title + "/" + content_files[0]
        else:
            for f in content_files:
                if f[-4:] == 'html':
                    content_path = "challenges_files/" + new_title + "/" + f

        # create the challenge object
        Challenge.objects.create(
            id_chall = id_challenge,
            type_chall = challenge_type,
            title = challenge_title,
            description = challenge_description,
            file_content = content_path,
            flag = sha256(challenge_flag.encode('utf-8')).hexdigest(),
            )

        id_challenge += 1

