import os, posixpath, argparse, subprocess

final_text_path = 'configuration/text/result/final.txt'
final_audio_path = 'configuration/voice/result/final.wav'
created_video_path = 'result/final_result.mp4'
edited_video_path = 'result/final_edit.mp4' 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'AI Generator and Video Editor by https://github.com/Omodaka9375')
    parser.add_argument('-i','--input-text', type = str, help = 'Starting words', required = True)
    parser.add_argument('-t','--title', type = str, help = 'Video title', required = False)
    parser.add_argument('-b','--background', type = str, help = 'Moving or static video background', required = False, default='configuration/background.jpg')
    parser.add_argument('-e','--edit', type = bool, help = 'Edit created video?', default=False, required = False)
    parser.add_argument('-et','--edit-type', type = str, help = 'Type of edit:silent or beep', default='silent', required = False)
    parser.add_argument('-st','--silent-threshold', type=float, default=0.03, help="Volume amount that frames' audio needs to surpass to be consider", required = False)
    parser.add_argument('-u','--upload', type = bool, help = 'Upload to YT immediatly?', default=False, required = False)
   
    parser.add_argument('-r','--repeater', help ='Reapeat every Nth word in list', type = int, default = 4,required = False)
    parser.add_argument('-d','--duration', help ='Duration images stay over screen', type = float, default = 2,required = False)
    parser.add_argument('-p','--position', help ='Position of overlayed image on the screen', type = int, default = 1,required = False)
    parser.add_argument('-l','--limit', help ='Limit how many images are downloaded per word', type = int, default= 4,required = False)

    args = parser.parse_args()

    subprocess.call('python3 configuration/text/createText.py "' + args.input_text + '"', shell=True)
    subprocess.call('python3 configuration/voice/createVoice.py',shell=True)
    subprocess.call('python3 AiGenerate.py -a ' + final_audio_path + ' -b ' + args.background + ' -r ' + str(args.repeater) + ' -d ' + str(args.duration) + ' -p ' + str(args.position) + ' -l ' + str(args.limit), shell=True)

    if args.edit:
        subprocess.call('python3 AiEdit.py -i ' + created_video_path + ' -t ' + args.edit_type + ' --silent_threshold ' + args.silent_threshold + ' -u ' + args.upload, shell=True)

    if args.upload==True and args.title:
        print ('Uploading to YT...')
        video_path=edited_video_path
        if not os.path.isfile(edited_video_path): 
            video_path=created_video_path    
        subprocess.call('youtube-upload --title="' + args.title + '" --auth-browser ' + video_path, shell=True)