import nltk
from datetime import datetime
from os import listdir, mkdir, remove
import extractImages
from subprocess import run
from PIL import Image

date = datetime.now().strftime('%Y-%m-%d')
path = f'/home/sr1/videoAUTO/News/{date}'
mkdir(f'{path}/Images')

files = []
for f in listdir(f'{path}/Articles'):
    if f.endswith('.txt') and f.startswith('HEADLINE') is not True:
        files.append(f)

for filename in files:
    filename = filename.replace('.txt', '')
    filename = filename.replace(';', ' ')
    filename = filename.replace("'", " ")

    tokens = nltk.word_tokenize(filename)

    # Article's headline is less than 6 words
    if len(tokens) < 6:

        images_path = f'{path}/Images/{filename}'

        mkdir(images_path)

        extractImages.run(filename, images_path, 10)

        # Removes corrupt image files
        for image in listdir(images_path):
            try:
                img = Image.open(f'{images_path}/{image}')
                img.verify()
            except Exception as e:
                print(e)
                remove(f'{images_path}/{image}')

        # print(images_path)
        # print(filename)

    # Article's headline more or equal to 6 words
    else:

        tagged_sent = nltk.pos_tag(tokens)

        # scope to further experiment
        proper_noun = [word for word, pos in tagged_sent if pos == 'NNP' or pos == 'NN' or pos == 'NNS' or pos == 'JJ' or pos == 'CD']

        nnp_string = ' '.join(list(dict.fromkeys(proper_noun)))

        images_path = f'{path}/Images/{filename}'

        mkdir(images_path)

        extractImages.run(nnp_string, images_path, 10)

        # Remove any corrupted image that might have downloaded
        for image in listdir(images_path):
            try:
                img = Image.open(f'{images_path}/{image}')
                img.verify()
            except Exception as e:
                print(e)
                remove(f'{images_path}/{image}')

        # print(images_path)
        # print(nnp_string)

# Renaming images with numbers in extension (ex: photo.jpg1)
try:
    run('./nameCleanup.sh')
except Exception as e:
    print(e)
    print('nameCleanup.sh script did not work!')


# To manually delete non-related images
print(f'\nCheck all your images before you continue.')
num = 1
for image_folders in listdir(f'{path}/Images'):
    print(f'\n\n{num}. {image_folders}')
    run(f'sxiv {path}/Images/"{image_folders}"/*', shell=True)
    num += 1
