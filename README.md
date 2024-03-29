# AIYA - Artificial Youtuber Project

This is a hobby project done in my spare time.

The basic idea is to create AI youtuber thats fully automated and can create daily videos on given subjects, voted by viewers. It's an attempt to create first artificial youtube personality that is fully autonomous as a content creator.

Ultimate idea is to use public blockchain voting mechanism as a means of deciding topics of upcomming videos. This would mean AI would be crypto driven by payments accumulated from willingfull participants in form of vote for suggested topic.

This project has wrapped up five different AI's to achieve it's goal (and a lot of ffmpeg!)

## Meet AIYA
![AIYA](./thumb.jpg)
## AIYA's demo video 
[![](http://img.youtube.com/vi/lzG6mV0qXAs/0.jpg)](https://youtu.be/lzG6mV0qXAs)
---------------------------------------------------------------
## Requirements
- Download and make Gentle (forced aligner): 
[https://github.com/lowerquality/gentle](https://github.com/lowerquality/gentle)

- Train and save GTP2 model checkpoint in 'configuration/text/checkpoint/'

You can use this Colab file to do so here:
[https://colab.research.google.com/github/Omodaka9375/GPT-2-Text-Generation/blob/master/GTP2.ipynb](https://colab.research.google.com/github/Omodaka9375/GPT-2-Text-Generation/blob/master/GTP2.ipynb)

or

If you want to reproduce same results you can use my model by downloading and unzipping this file in 'configuration/text' folder: [https://drive.google.com/file/d/1-0SHdVVcxVa5I3sopWywNzjoi9qWTKBW/view?usp=sharing](https://drive.google.com/file/d/1-0SHdVVcxVa5I3sopWywNzjoi9qWTKBW/view?usp=sharing)
- Train and download TTS PWGAN model by following instructions in 'configuration/voice/createVoice.py'
- Install spaCy: [https://github.com/explosion/spaCy](https://github.com/explosion/spaCy)
- Go to Google Cloud Text-to-Speech and create an API key: [https://cloud.google.com/speech-to-text/](https://cloud.google.com/speech-to-text/) 
- Follow this guide to create credentials for YT upload: [https://github.com/tokland/youtube-upload/](https://github.com/tokland/youtube-upload/)
---------------------------------------------------------------
## Basic usage (Python 3.6 =>)
1. Install dependencies
> pip3 install -r requirements.txt
2. Spin up Gentle docker image on localhost (in one terminal)
> docker run --network host -P lowerquality/gentle
3. In project root folder execute this command, while replacing the value of '-i' (in different terminal)
> python3 aiya.py -i "Love is"
4. Result will be in './result' folder
5. For uploding to YT, fill the credentials file in 'configuration/ytcreds/' and enter -u parameter as 'True' 
---------------------------------------------------------------
## Features
- Create YT like video from a phrase or a term
- Supports video or image background
- Overlay images over static image background
- Overlay images over video
- Randomization on run (different text everytime you run it)
- Control duration of visibility of memes
- Control density of memes
- Control positioning of memes
- Directly upload to YT
- Create thumbnail
- Support title adding as parametar
---------------------------------------------------------------
## TODO
- Better error handling
- Add support for image animation (rolling picture, popups, transition style), e.g.,
> ffmpeg -i out.mp4 -i images/bicycle.png -filter_complex "[1] scale=100:100 [tmp]; [0][tmp] overlay=x='if(gte(t,2), t*100, 10)':y=30" outputfile.mp4
- Add support for random zoom in effects
- Include phrases not just verbs in the bag
- Add support for loading marked or unmarked text directly
- Add support for blockchain or twitter voting
- Train better voice model
- Train GTP-2 model with more data
- Replace Bing as image searcher
- Add face to the voice
---------------------------------------------------------------
## Troubleshoting
- If proces ends with error, it is mostly due to corrupted images that were randomly picked or while downloading. You can increase the number of imager per term using '-l' parameter, default is 4, and re-run the script.
- Most customizations can be done using parameters. Check 'aiya.py' for usage and optional parametars.
- If the generated sentences are too long they will be cut at the end :(
---------------------------------------------------------------
## AI stack
- OpeAI GTP-2 774M model trained in Google collab: [https://github.com/openai/gpt-2](https://github.com/openai/gpt-2) [**for text creation**]
- Google Speech Recognizer: [https://cloud.google.com/speech-to-text/](https://cloud.google.com/speech-to-text/) [**for speech to text**]
- Gentle: [https://github.com/lowerquality/gentle](https://github.com/lowerquality/gentle) [**for timed transcription from audio**]
- SpaCy: [https://github.com/explosion/spaCy](https://github.com/explosion/spaCy) [**for noun/verbs extraction**]
- TTS ParallelWave GAN model:[https://github.com/kan-bayashi/ParallelWaveGAN](https://github.com/kan-bayashi/ParallelWaveGAN) [**for generating voice from text**]
---------------------------------------------------------------
## Contact
- branislav.djalic@gmail.com
---------------------------------------------------------------
## Contributions
Feel free to contribute, comment, improve or make your own AI youtuber ;)