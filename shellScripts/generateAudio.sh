#!/bin/bash

# Makes a audio directory
# Generate audio for each articles in the Articles directory using google TTS
# Also generate separare headline for each articles
# Finally mix the Backgound music with the articles audio using mixAudio.sh

cd ../News/$(date +"%Y-%m-%d")
mkdir audio
cd audio

for file in ../Articles/*.txt;
do

    python ~/videoAUTO/scripts/pythonScripts/synthesize_file.py --ssml "$file";
    sleep 2;

done

mkdir HEADLINES
mv HEADLINE*.mp3 HEADLINES

mkdir tempAudio;
for audio in *.mp3;
do

    ~/videoAUTO/scripts/shellScripts/mixAudio.sh "$audio" tempAudio/"$audio";
    rm "$audio";
    mv tempAudio/"$audio" .;

done
rm -rf tempAudio;
