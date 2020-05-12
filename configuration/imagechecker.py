import os
from subprocess import Popen, PIPE
import tensorflow as tf

folderToCheck = 'configuration/images/'
fileExtension = '.jpg'

def checkImage(fn):
  proc = Popen(['identify', '-verbose', fn], stdout=PIPE, stderr=PIPE)
  out, err = proc.communicate()
  exitcode = proc.returncode
  return exitcode, out, err

num_skipped = 0

for directory, subdirectories, files, in os.walk(folderToCheck):
  for file in files:

    if file.endswith(fileExtension):
      filePath = os.path.join(directory, file)
      code, output, error = checkImage(filePath)
      if str(code) !="0" or str(error, "utf-8") != "":
        print("ERROR " + filePath)
        os.remove(filePath)
      else:
        print("OK " + filePath)
    else: 
      filePath = os.path.join(directory, file)
      os.remove(filePath)

    
    if tf.compat.as_bytes('JFIF') not in os.path.join(directory, file).peek(10):
      num_skipped += 1
      filePath = os.path.join(directory, file)
      os.remove(filePath)
      # Delete corrupted image  

print('Deleted %d images' % num_skipped)
print("-------------- DONE --------------")