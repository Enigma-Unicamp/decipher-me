import string
import random
import sys

# Check if user has passed only secretkey.txt path. It should be something
# like 'decipher/secretkey.txt'
if (len(sys.argv) != 2):
  print("Error: you should pass me only the secretkey.txt file path")
  sys.exit()

# Get filepath
filePath = sys.argv[1]

# Generate the key using sys random (which is safer)
generatedKey = ''.join([random.SystemRandom().choice(string.ascii_letters +
                        string.digits + string.punctuation) for _ in range(50)])

# Open the file, write the key and then close it
secretFile = open(filePath, 'w')
secretFile.write(generatedKey)
secretFile.close()

