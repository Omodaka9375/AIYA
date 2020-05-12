import os, posixpath, argparse, subprocess

# example command to run
#python3 AiEdit.py -t silent -i test/raw_video games.mp4 -u True --silent_threshold 0.1
#python3 AiEdit.py -t beep -i test/raw_video games.mp4

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'AI Video Editor')
    parser.add_argument('-t','--cut_type', type=str, help = 'Use silente or beep cutter', required = True)

    parser.add_argument('-i','--input_file', type=str,  help='Video file you want modified',required = True)

    parser.add_argument('-u','--upload', type=bool,  help='Upload to youtube immediately?',required = False, default=False)
    # jumpcutter options
    parser.add_argument('--url', type=str, help='A youtube url to download and process', required = False)
    parser.add_argument('--output_file', type=str, default="result/final_edit.mp4", help="the output file. (optional. if not included, it'll just modify the input file name)", required = False)
    parser.add_argument('--silent_threshold', type=float, default=0.03, help="the volume amount that frames' audio needs to surpass to be consider \"sounded\". It ranges from 0 (silence) to 1 (max volume)", required = False)
    parser.add_argument('--sounded_speed', type=float, default=1.00, help="the speed that sounded (spoken) frames should be played at. Typically 1.", required = False)
    parser.add_argument('--silent_speed', type=float, default=5.00, help="the speed that silent frames should be played at. 999999 for jumpcutting.", required = False)
    parser.add_argument('--frame_margin', type=float, default=1, help="some silent frames adjacent to sounded frames are included to provide context. How many frames on either the side of speech should be included? That's this variable.", required = False)
    parser.add_argument('--sample_rate', type=float, default=44100, help="sample rate of the input and output videos", required = False)
    parser.add_argument('--frame_rate', type=float, default=30, help="frame rate of the input and output videos. optional... I try to find it out myself, but it doesn't always work.", required = False)
    parser.add_argument('--frame_quality', type=int, default=3, help="quality of frames to be extracted from input video. 1 is highest, 31 is lowest, 3 is the default.", required = False)
    # beepcuter options
    parser.add_argument('--output_dir', type=str, default='configuration/videos', help="for cutted videos before joining", required = False)
    parser.add_argument('--output_format', type=str, default='mp4', required=False)

    args = parser.parse_args()
    if 'silent' in args.cut_type:
        subprocess.call('python3 configuration/jumpcutter.py -i ' + args.input_file + ' --output_file ' + args.output_file  + ' --silent_threshold ' + str(args.silent_threshold) + ' --sounded_speed ' + str(args.sounded_speed) + ' --silent_speed ' + str(args.silent_speed) + ' --frame_margin ' + str(args.frame_margin) + ' --sample_rate ' + str(args.sample_rate) + ' --frame_rate ' + str(args.frame_rate) + ' --frame_quality ' + str(args.frame_quality), shell=True)
    elif 'beep' in args.cut_type:
        subprocess.call('python3 configuration/beepcutter.py ' + args.input_file + ' ' + args.output_dir + ' ' + args.output_format, shell=True)
    else: 
        print('\nError in selecting cutting type. Please, select "silent" or "beep"') 
        exit(0)