#!/bin/bash

# Main script that executes all the following scripts required

echo;
echo "+++++++++++++++++++++++++++++++
++++++ Scraping Articles ++++++
+++++++++++++++++++++++++++++++";
echo;

python pythonScripts/scrapARTICLES.py;

echo;
echo "++++++++++++++++++++++++++++++
++++++ Generating Audio ++++++
++++++++++++++++++++++++++++++";
echo;

shellScripts/generateAudio.sh;

echo;
echo "+++++++++++++++++++++++++++++++++
++++++++ Scraping Images ++++++++
+++++++++++++++++++++++++++++++++";

python pythonScripts/images.py

echo;
echo "++++++++++++++++++++++++++++++
++++++ Generating Video ++++++
++++++++++++++++++++++++++++++";

python pythonScripts/generateVideo.py;

echo;
