# $1 - Main audio file (Ex: the news reporting)
# $2 - Final audio file to be saved with the main audio & bg sound

# Calculate length of the audio
length=`mp3info -p "%m:%02s\n" "$1"`

# Output BG audio file with trimmed length
output="trimBG.mp3"

# Background audio file
ogfile="/home/sr1/videoAUTO/scripts/mediaFiles/bgNEWS.mp3"

ffmpeg -i "$ogfile" -ss 00:00:00 -to "$length" -c copy "$output" > /dev/null 2>&1;

ffmpeg -i "$1" -i "$output" -filter_complex amerge -ac 2 -c:a libmp3lame -q:a 4 "$2" > /dev/null 2>&1;

rm "$output";

