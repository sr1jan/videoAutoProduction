# videoAutoProduction
### A simple program to automate production of news videos for a youtube channel written in python and bash

The code that I have written is for a specific topic, website and video. So keep that in mind if you are using it and make changes likewise.


**Requirements**

1. ffmpeg
2. moviepy
3. beautifulsoup
4. urlib.request 
5. wget
6. nltk
7. request
8. xml.dom.minidom.parseString
9. gcp's texttospeech API


**Setup**

Run these commands one by one to setup the program in a file structure that is required by the code to run.

```bash
cd ~
git clone https://github.com/sr1jan/videoAutoProduction
mkdir videoAuto
cd videoAuto
mkdir News scripts
mv ../videoAutoProduction/* ./scripts/
rm -rf ~/videoAutoProduction
cd scripts
```

Make sure you have all the requirements and also you have to tinker the code a little bit to make it work locally and for your purpose. 

Things you need to do:
+ Change `/home/sr1` in the codebase to `home/<yourUserName>` everywhere.
+ Have to get your API key from *smmry.com* and save it in a yaml file. Then access that key in the **scrapArticles.py** file.Refer the code to understand.
+ Also you have to setup and configure your account on *Google cloud platform* and get the [texttospeech API](https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries) to work in your machine.
+ *will add more once I come across more edge cases* 

You can execute the program by running the `autoVideo.sh` script.

