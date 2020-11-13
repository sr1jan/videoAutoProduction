from os import listdir, mkdir, chdir
from subprocess import run
from datetime import datetime
from moviepy.editor import VideoFileClip, TextClip, AudioFileClip, CompositeVideoClip, ImageClip, concatenate_videoclips


date = datetime.now().strftime('%Y-%m-%d')
path = f'/home/sr1/Projects/Others/videoAUTO/News/{date}'
chdir(path)
mkdir(f'{path}/Videos')

# generating videos from images with fade transition
for images_folder in listdir(f'{path}/Images'):
    pics_count = len(listdir(f'{path}/Images/{images_folder}'))
    if pics_count is 0: continue
    audio_length = int(run(["mp3info", "-p", "% S", f'{path}/audio/{images_folder}.mp3'], capture_output=True, text=True).stdout)
    image_duration = float(f'{audio_length - 2.0 * pics_count}')
    image_duration = float(f'{image_duration/pics_count}')

    try:
        run(['/home/sr1/Projects/Others/videoAUTO/scripts/shellScripts/videoOutput.sh', f'"{images_folder}"', f'{image_duration}', f'{path}/Images/{images_folder}'])
    except Exception as e:
        print(e)


chdir(f'{path}/Videos')
mkdir('tmpVids')

for mp4 in listdir('.'):
    if mp4.endswith('.mp4'):
        run(['mv', f'{mp4}', 'tmpVids'])

# adding audio to videos generated through the images
for vids in listdir('./tmpVids'):
    run(['ffmpeg', '-i', f'./tmpVids/{vids}', '-i', f'../audio/{vids[:-4]}.mp3', '-c', 'copy', f'{vids}'])

run(['rm', '-rf', './tmpVids'])

mkdir('tmpVids')
chdir('tmpVids')

# adding headline to each video
videos_list = []
num = 1
transition_clip = VideoFileClip('/home/sr1/Projects/Others/videoAUTO/scripts/mediaFiles/transition.mp4')
for videos in listdir('..'):
    if videos.endswith('.mp4'):
        headline_audio = 'HEADLINE-' + videos[:-4] + '.mp3'
        audio = AudioFileClip(f'{path}/audio/HEADLINES/{headline_audio}')
        audio_duration = int(run(["mp3info", "-p", "% S", f'{path}/audio/HEADLINES/{headline_audio}'], capture_output=True, text=True).stdout) + 1

        healine_txt = f'{num}.\n\n{videos[:-4]}'
        text_clip = TextClip(healine_txt, size=(1024, 200), color='white', font='ADAM.CG PRO', kerning=2, method='caption', align='center').set_pos("center")
        text_clip = text_clip.set_duration(audio_duration)
        text_clip = text_clip.set_audio(audio)

        video_clip = VideoFileClip(f'../{videos}')
        video_duration = video_clip.duration

        isf_logo = ImageClip('/home/sr1/Projects/Others/videoAUTO/scripts/mediaFiles/isf.png').set_duration(video_duration)

        render = CompositeVideoClip([video_clip.set_start(audio_duration), isf_logo.set_start(audio_duration).set_pos(('left', 'bottom')), text_clip.crossfadein(1).crossfadeout(1)], bg_color=[128, 0, 0])
        render.write_videofile(f'{num}.mp4')

        videos_list.append(f'{num}.mp4')
        num += 1

run('rm ../*.mp4', shell=True)
run('mv *.mp4 ../.', shell=True)
chdir('..')
run(['rm', '-rf', './tmpVids'])

videos = []
for video in videos_list:
    video = VideoFileClip(video)
    videos.append(video)

news = concatenate_videoclips(videos, transition=transition_clip)
news.write_videofile(f'videos.mp4')

news_clip = VideoFileClip('videos.mp4')
intro_clip = VideoFileClip(f'/home/sr1/Projects/Others/videoAUTO/scripts/mediaFiles/introISF.mp4').set_pos('center')
subscribe_clip = VideoFileClip(f'/home/sr1/Projects/Others/videoAUTO/scripts/mediaFiles/subs.mp4', audio=False).set_pos('center')

final_video = CompositeVideoClip([news_clip.set_start(subscribe_clip.duration + 2 + intro_clip.duration + 2), intro_clip.set_start(subscribe_clip.duration + 2), subscribe_clip.crossfadeout(1)])
final_video.write_videofile(f'{date}.mp4')
