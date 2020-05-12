from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
import os
import glob
from sys import argv
import speech_recognition as sr
import shutil
import random
from random import randrange
import json
import soundfile as sf
import spacy
import subprocess
import datetime
from pathlib import Path
from PIL import Image
import shlex

#python3 configuration/grippa.py configuration/voice/result/final.wav configuration/background.jpg 3 1.2 1 4

# set some vars
background=str(argv[2])
repeater=int(argv[3])
speed=float(argv[4])
position=int(argv[5])
limit=int(argv[6])

googlekey='<YOUR-GOOGLE-CLOUD-SPEECH-KEY>'
# cleanup previous results
if os.path.exists('configuration/result'):
    shutil.rmtree('configuration/result')

recognised_text = ''
# get audio from arv[1] and transcribe it to a text file
r = sr.Recognizer()

print('\nTranscribing audio source ' + argv[1])

with sr.AudioFile(argv[1]) as source:
	audio = r.record(source)

try:
	recognised_text = r.recognize_google(audio, key=googlekey)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

if len(recognised_text)<=0:
	print('Error in text size.')
	exit(0)

with open("configuration/transcript.txt", "w") as text_file:
    text_file.write(recognised_text)

print("\nTranscription saved to file")
print("\nRecognized text: \n" + recognised_text)

# unite verbs and nouns and extract verbs and nouns
nlp = spacy.load("en_core_web_sm")
doc = nlp(recognised_text)

# analyze syntax
print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

phrases = [token.lemma_ for token in doc if token.pos_ == "VERB"]
nouns = [chunk.text for chunk in doc.noun_chunks]

# save mp3 version
subprocess.call('ffmpeg -i ' + argv[1] + ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 configuration/track.mp3', shell=True)
print("\nOriginal wav, converted to mp3")

# take audio + text and get timestamps from Gentle API
subprocess.call('curl -F "audio=@configuration/track.mp3" -F "transcript=@configuration/transcript.txt" "http://localhost:8765/transcriptions?async=false" -o "configuration/result.json"', shell=True)
print("\nFetched timestamps for audio transcription")

# take json object, serialize it ang itterate through it
data = ''
key_list = []
value_list = []

with open('configuration/result.json') as json_file:
	data = json.load(json_file)

for p in data['words']:
	if p['word'] in phrases and p['word'] not in key_list and "start" in p:
		# if len(wd) > 3 and "*" not in wd and "start" in p:
		key_list.append(p['word'].lower())
		print('Word: ' + p['word'])
		value_list.append(float(p['start']))

print("\nNum. of phrases found: " + str(len(key_list)))


# pick every n-th keywor skipping first two
small_list = key_list[1::]#repeater]
big_list = value_list[1::]#repeater]
print("\nNum. of words chosen: " + str(len(small_list)))
print("\nWords chosen: " + str(small_list))

# couple keys and values in a dict
timetable=dict(zip(small_list,big_list))

# get google images for each word and store in /images folder
print("\nCleanup some folders...")
if os.path.exists('configuration/images'):
    shutil.rmtree('configuration/images')

# get all words in one file and send it to bulk downloader
with open('configuration/search_dump', 'w') as f:
    for item in small_list:
        f.write("%s\n" % item)

print("\nStart downloading images...")
subprocess.call("python3 configuration/imagedownloader.py -f 'configuration/search_dump' -o 'configuration/images' --limit " + str(limit) +" --threads 40", shell=True)
print("\nDownloading images done")

# get lenght of provided audio file
f = sf.SoundFile(argv[1])
seconds_ = len(f) / f.samplerate
time = str(datetime.timedelta(seconds=seconds_))
print('\nAudio track lenght (seconds) = {}'.format(seconds_))

if '.mp4' in background:
	subprocess.call('ffmpeg -i ' + background + ' -an configuration/output.mov', shell=True)
elif '.jpg' in background:
	subprocess.call('ffmpeg -loop 1 -r 1 -i ' + background + ' -t %s' % time + ' -vcodec qtrle -an configuration/output.mov', shell=True)
else:
	print('Error: Please provide proper format for the background. mp4 or jpg') 
	exit(0)

subprocess.call('ffmpeg -i configuration/output.mov -q:v 0 configuration/out.mp4', shell=True)
print('\nCreated a video clip from image backgound provided')

# get video height and width
cmd = "ffprobe -v quiet -print_format json -show_streams"
args = shlex.split(cmd)
args.append('configuration/out.mp4')

# run the ffprobe process, decode stdout into utf-8 & convert to JSON
ffprobeOutput = subprocess.check_output(args).decode('utf-8')
ffprobeOutput = json.loads(ffprobeOutput)

# find height and width
height = ffprobeOutput['streams'][0]['height']
width = ffprobeOutput['streams'][0]['width']
print('\nVideo width: ' + str(width))
print('Video height: ' + str(height))

# overlay positioning
centered='overlay=('+ str(width) +'-w)/2:(' + str(height) +'-h)/2' #1
top_left='overlay=0:0' #2
top_right='overlay='+ str(height) +'-w-5:5' #3
bottom_right='overlay='+ str(width) +'-w-5:'+ str(height) +'-h-5' #4
bottom_left='overlay=5:'+ str(height) +'-h-5' #5

overlay=''

if position == 1:
	overlay=centered
elif position == 2:
	overlay=top_left
elif position == 3:
	overlay=top_right
elif position == 4:
	overlay=bottom_right
elif position == 5:
	overlay=bottom_left
else: position=1

# do images cleanup
names = []
values = []
for i in timetable: 
	names.append(i)
	values.append(timetable[i])

for i in range(0,len(names)):
	for file in glob.glob('configuration/images/' + names[i] + '/*.png'):
		im = Image.open(file)
		if im.size[1] > height:
			new_width  = height * im.size[0] / im.size[1]
			im = im.resize((int(new_width), int(height)))

		rgb_im = im.convert('RGB')
		rgb_im.save(file.replace("png", "jpg"), quality=95)

	for file in glob.glob('configuration/images/' + names[i] + '/*.PNG'):
		im = Image.open(file)

		if im.size[1] > height:
			new_width  = height * im.size[0] / im.size[1]
			im = im.resize((int(new_width), int(height)))
		
		rgb_im = im.convert('RGB')
		rgb_im.save(file.replace("PNG", "jpg"), quality=95)

	for file in glob.glob('configuration/images/' + names[i] + '/*.jpeg'):
		im = Image.open(file)

		if im.size[1] > height:
			new_width  = height * im.size[0] / im.size[1]
			im = im.resize((int(new_width), int(height)))

		rgb_im = im.convert('RGB')
		rgb_im.save(file.replace("jpeg", "jpg"), quality=95)

	for file in glob.glob('configuration/images/' + names[i] + '/*.JPEG'):
		im = Image.open(file)

		if im.size[1] > height:
			new_width  = height * im.size[0] / im.size[1]
			im = im.resize((int(new_width), int(height)))

		rgb_im = im.convert('RGB')
		rgb_im.save(file.replace("JPEG", "jpg"), quality=95)

	for file in glob.glob('configuration/images/' + names[i] + '/*.JPG'):
		im = Image.open(file)

		if im.size[1] > height:
			new_width  = height * im.size[0] / im.size[1]
			im = im.resize((int(new_width), int(height)))

		rgb_im = im.convert('RGB')
		rgb_im.save(file.replace("JPG", "jpg"), quality=95)

	for file in glob.glob('configuration/images/' + names[i] + '/*.gif'):
		im = Image.open(file)

		if im.size[1] > height:
			new_width  = height * im.size[0] / im.size[1]
			im = im.resize((int(new_width), int(height)))

		rgb_im = im.convert('RGB')
		rgb_im.save(file.replace("gif", "jpg"), quality=95)

	for file in glob.glob('configuration/images/' + names[i] + '/*.GIF'):
		im = Image.open(file)

		if im.size[1] > height:
			new_width  = height * im.size[0] / im.size[1]
			im = im.resize((int(new_width), int(height)))

		rgb_im = im.convert('RGB')
		rgb_im.save(file.replace("GIF", "jpg"), quality=95)
	
	for file in glob.glob('configuration/images/' + names[i] + '/*.tif'):
		im = Image.open(file)

		if im.size[1] > height:
			new_width  = height * im.size[0] / im.size[1]
			im = im.resize((int(new_width), int(height)))

		rgb_im = im.convert('RGB')
		rgb_im.save(file.replace("GIF", "jpg"))

	for file in glob.glob('configuration/images/' + names[i] + '/*.TIF'):
		im = Image.open(file)

		if im.size[1] > height:
			new_width  = height * im.size[0] / im.size[1]
			im = im.resize((int(new_width), int(height)))

		rgb_im = im.convert('RGB')
		rgb_im.save(file.replace("GIF", "jpg"), quality=95)

print('\nImage conversion done')
# check images
subprocess.call("python3 configuration/imagechecker.py", shell=True)
print("\nAll images checked")

# fix image names
for directory, subdirectories, files, in os.walk('configuration/images'):
  for file in files:
	  if '*' or '(' or ')' or '%' in file:
		  absname = os.path.join(directory, file)
		  newname = os.path.join(directory, file.replace('(','').replace(')','').replace('*','').replace('+','').replace('%',''))
		  os.rename(absname, newname)

# start creating ffmpeg command from dict
images_ = []
for i in range(0,len(names)):
	myImages = glob.glob('configuration/images/' + names[i] + '/*.jpg')
	if myImages:
		images_.append(myImages[randrange(len(myImages))])

part1 = []
part2 = []

for i in range(0,len(images_)):
	part1.append(' -i ' + images_[i])

all_imgs = "".join(part1)
lineOne = 'ffmpeg -i configuration/out.mp4' + all_imgs + ' -filter_complex '
sep = '"'

for i in range(0,len(values)):
	if len(values) == 1:
		part2.append("[v" + str(i) + "][" + str(i+1) + "] " + overlay + ":enable='between(t," + str(int(round(float(values[i])))) + "," + str(int(round(float(values[i])))+speed) + ")'[v" + str(i+1) + "]")
	elif i == 0:
		part2.append("[" + str(i) + "][" + str(i+1) + "] " + overlay + ":enable='between(t," + str(int(round(float(values[i])))) + "," + str(int(round(float(values[i])))+speed) + ")'[v" + str(i+1) + "];")
	elif i==(len(values)-1):
		part2.append("[v" + str(i) + "][" + str(i+1) + "] " + overlay + ":enable='between(t," + str(int(round(float(values[i])))) + "," + str(int(round(float(values[i])))+speed) + ")'[v" + str(i+1) + "]")
	else: 
		part2.append("[v" + str(i) + "][" + str(i+1) + "] " + overlay + ":enable='between(t," + str(int(round(float(values[i])))) + "," + str(int(round(float(values[i])))+speed) + ")'[v" + str(i+1) + "];")

lineTwo = "".join(part2)
lineThree = ' -map "[v'+ str(len(values)) + ']"' + ' configuration/result.mp4'

command = lineOne + sep + lineTwo + sep + lineThree
#print('\nCommand: \n'+ command)
subprocess.call(command,shell=True)
print('\nVideo creation process finished')

if not os.path.exists('result'):
    os.makedirs('result')
else:
	shutil.rmtree('result')
	os.makedirs('result')

# combine created video and audio
subprocess.call('ffmpeg -i configuration/result.mp4 -i configuration/track.mp3 -c copy -map 0:v:0 -map 1:a:0 result/final_result.mp4', shell=True)
print('\nCombining video and audio tracks')

# create thumbnail
subprocess.call('ffmpeg -i result/final_result.mp4 -ss 00:00:10 -vframes 1 result/thumbnail.png', shell=True)
print('\nCreated thumbnail')

# cleanup all files 
print('\nDoing some housekeeping')
os.remove('configuration/transcript.txt')
os.remove('configuration/search_dump')
os.remove('configuration/result.json')
os.remove('configuration/track.mp3')
os.remove('configuration/output.mov')
os.remove('configuration/out.mp4')
os.remove('configuration/result.mp4')
if os.path.exists('configuration/images'):
    shutil.rmtree('configuration/images')

print ('\nDone. Take a look at result folder\n')