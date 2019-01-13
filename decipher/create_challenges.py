import os
import csv
from challenge.models import Challenge
from hashlib import sha256

# list all challenges directories
challenges_dirs = os.listdir("../challenge/static/challenges_files")

# iterate through all challenges
id_challenge = 0
for challenge_dir in challenges_dirs:

    # challenge folder
    challenge_path = "../challenge/static/challenges_files/" + challenge_dir

    # settings file path
    settings_path = challenge_path + "/settings.csv"

    # the "other file" path
    other_file_path = os.listdir(challenge_path)
    other_file_path.remove("settings.csv")
    other_file_path = "challenges_files/" + challenge_dir + "/" + other_file_path[0]

    print(other_file_path)

    # open settings file
    with open(settings_path, 'r') as settings_file:

        reader = csv.reader(settings_file)
        settings = next(reader)

        # each challenge setting
        challenge_type  = settings[0]
        challenge_title = settings[1]
        challenge_flag  = settings[2]
        challenge_description = settings[3]

        Challenge.objects.create(
            id_chall = id_challenge,
            type_chall = challenge_type,
            title = challenge_title,
            description = challenge_description,
            file_content = other_file_path,
            flag = sha256(challenge_flag.encode('utf-8')).hexdigest(),
            )
  
    id_challenge += 1


    
