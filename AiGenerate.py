import os, posixpath, argparse, subprocess
#example command to run
#python3 AiGenerate.py -a test/audio/games.wav -b test/raw_video games.mp4 -r 3 -d 1.2 -p 1 -l 4

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'AI Generator and editor')
    parser.add_argument('-a','--input-audio', help = 'Audio file with speech', required = True)
    parser.add_argument('-b','--input-background', help = 'Image or video file to apply in background', required = False)
    parser.add_argument('-r','--repeater', help ='Reapeat every Nth word in list', type = int, default = 4,required = False)
    parser.add_argument('-d','--duration', help ='Duration images stay over screen', type = float, default = 2,required = False)
    parser.add_argument('-p','--position', help ='Position of overlayed image on the screen', type = int, default = 1,required = False)
    parser.add_argument('-l','--limit', help ='Limit how many images are downloaded per word', type = int, default= 3,required = False)

    args = parser.parse_args()
    if (not args.input_audio) and (not args.input_background):
        parser.error('Provide audio file path and provide background for the video and try again.')
        exit(0)
    else:
        subprocess.call('python3 configuration/main.py ' + args.input_audio + ' ' + args.input_background + ' ' + str(args.repeater) + ' ' + str(args.duration) + ' ' + str(args.position) + ' ' + str(args.limit), shell=True)
