#!/bin/bash

# Main script that executes all the following scripts required

echo;
echo "+++++++++++++++++++++++++++++++
++++++ Scraping Articles ++++++
+++++++++++++++++++++++++++++++";
echo;

python scrapARTICLES.py;

echo;
echo "++++++++++++++++++++++++++++++
++++++ Generating Audio ++++++
++++++++++++++++++++++++++++++";
echo;

./generateAudio.sh;

echo;
echo "+++++++++++++++++++++++++++++++++
++++++++ Scraping Images ++++++++
+++++++++++++++++++++++++++++++++";

python images.py

echo;
echo "++++++++++++++++++++++++++++++
++++++ Generating Video ++++++
++++++++++++++++++++++++++++++";

python generateVideo.py;

echo;
