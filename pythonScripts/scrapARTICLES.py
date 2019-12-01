from bs4 import BeautifulSoup, SoupStrainer
import requests
import os
from datetime import datetime
import re
import yaml
import time
import urllib.request
from xml.dom.minidom import parseString
import csv


date = datetime.now().strftime('%Y-%m-%d')
# day = datetime.now().strftime('%d')
os.mkdir(f'/home/sr1/videoAUTO/News/{date}')
os.mkdir(f'/home/sr1/videoAUTO/News/{date}/Articles')
os.chdir(f'/home/sr1/videoAUTO/News/{date}/Articles')

# API key for smmry.com saved in a yml file
creds = yaml.load(open('/home/sr1/.config/.credentials.yml'), Loader=yaml.BaseLoader)
key = creds['smmry']['key'][0]

# article scraping source
parentURL = "https://news.google.com/rss/search?q=%20site%3Ahttps%3A%2F%2Feconomictimes.indiatimes.com%2Fnews%2Fdefence%20when%3A1d&hl=en-IN&gl=IN&ceid=IN%3Aen"

# mainREQ = requests.get(parentURL)

feed = {}
feed_list = []
with urllib.request.urlopen(parentURL) as f:
    # print(f.read().decode('utf-8'))
    dom = parseString(f.read())
    status = f.status

    try:
        if status == 200:
            print('Website Exists!\n')
    except Exception as e:
        print(e)
        print('Invalid Website URL!')
        exit()

    # node which have the articles
    items = dom.getElementsByTagName("item")

    count = 1
    for item in items:
        title = item.getElementsByTagName('title')[0].childNodes[0].data
        date = item.getElementsByTagName('pubDate')[0].childNodes[0].data
        link = item.getElementsByTagName('link')[0].childNodes[0].data
        if 'Watch' in title or 'View' in title:
            continue
        title = title.replace(" - Economic Times", "")

        # print(title)
        # print("Title: %s" % title.childNodes[0].data)
        # print(date)
        # print(link)

        feed['Title'] = title
        feed['Link'] = link
        feed['Published Date'] = date

        feed_list.append(feed)
        feed = {}

        # limiting max articles to be scraped
        if count >= 4:
            break
        count += 1

if feed_list is None:
    print('No article availale right now')
    exit()

num = 1
error = 0
for data in feed_list:
    link = data['Link']
    title = data['Title']

    # using smmry.com to summarise articles
    url = "https://api.smmry.com"

    params = {'SM_API_KEY': key,
              'SM_WITH_BREAK': '\n',
              'SM_LENGTH': 7,
              'SM_URL': link}

    req = requests.post(url=url, params=params)
    smmry = req.json()

    if 'sm_api_error' in smmry:

        errorCODES = [0, 1, 2, 3]
        if (smmry['sm_api_error']) in errorCODES and (smmry['sm_api_error']) != 3:

            if (smmry['sm_api_error']) == 2:
                print(f"\nERROR: {smmry['sm_api_message']}")
                print('Issue with your API account, probably you ran out of the daily limit')
                exit()

            elif (smmry['sm_api_error']) == 1:
                print(f'\nERROR: {smmry["sm_api_message"]} \n')
                print(f"Something wrong with the parameters you\'re passing with the URL")
                exit()

        # summarization error probably due to article being too short
        elif (smmry['sm_api_error']) == 3:

            try:

                req = requests.get(link)
                article_content = SoupStrainer('div', class_='relative')
                soup = BeautifulSoup(req.text, "html.parser", parse_only=article_content)

                body = soup.find('div', class_='Normal').text

                # Using regex to clean & structure the article's paragraphs
                # Removes the advertisement code
                # body = re.sub(r'\<br\/\>\<br\/\>\<script.*\<\/script\>\<br\/\>\<br\/\>', '', body)
                # body = body.replace('<p>', '')
                # body = body.replace('</p>', '')
                # body = body.replace('<br/><br/>', '\n')

                filename = title + '.txt'
                headline = 'HEADLINE-' + title + '.txt'

                with open(headline, 'w') as fp:
                    headline = headline.replace('.txt', '')
                    headline = headline.replace('HEADLINE-', '')

                    # data cleaning and SSML insertion for TTS purpose
                    try:
                        words = []
                        for word in re.findall(r'[A-Z]{2,7}', headline):
                            if word in words:
                                continue
                            headline = re.sub(f'{word}', f'<say-as interpret-as="characters">{word}</say-as>', headline)
                            words.append(word)
                    except Exception:
                        pass

                    fp.write('<speak>')
                    fp.write(headline)
                    fp.write('</speak>')

                # data cleaning and SSML insertion for TTS purpose
                with open(filename, 'w') as fp:
                    try:
                        words = []
                        for word in re.findall(r'[A-Z]{2,7}', body):
                            if word in words:
                                continue
                            body = re.sub(f'{word}', f'<say-as interpret-as="characters">{word}</say-as>', body)
                            words.append(word)
                    except Exception:
                        pass

                    fp.write('<speak>\n')

                    for line in body.splitlines():
                        line = '<s>' + line + '</s>' + '\n'
                        fp.write(line)

                    fp.write('</speak>')

                print(f'Article {[num]} : Summarized & Saved [Short]')
                num += 1
                time.sleep(3)

                continue

            except Exception as e:
                print(f'Article {[num]} : ERROR - {e}')
                num += 1
                error += 1
                continue

    # no error with smmry
    else:

        filename = title + '.txt'
        headline = 'HEADLINE-' + title + '.txt'

        with open(headline, 'w') as fp:
            headline = headline.replace('.txt', '')
            headline = headline.replace('HEADLINE-', '')

            # data cleaning and SSML insertion for TTS purpose
            try:
                words = []
                for word in re.findall(r'[A-Z]{2,7}', headline):
                    if word in words:
                        continue
                    headline = re.sub(f'{word}', f'<say-as interpret-as="characters">{word}</say-as>', headline)
                    words.append(word)
            except Exception:
                pass

            fp.write('<speak>')
            fp.write(headline)
            fp.write('</speak>')

        with open(filename, 'w') as fp:
            data = smmry['sm_api_content']
            data = data.replace('[BREAK]', '\n')

            # data cleaning and SSML insertion for TTS purpose
            try:
                data = re.sub(r'[A-Z0-9\s]+:', '', data)
            except Exception:
                pass

            data = re.sub(r'^\s', '', data, flags=re.MULTILINE)

            try:
                data = data.replace('BCCL.', '')
                data = re.sub(r'\s[0-9]\.\/[0-9]\.', '', data)
            except Exception:
                pass

            try:
                words = []
                for word in re.findall(r'[A-Z]{2,7}', data):
                    if word in words:
                        continue
                    data = re.sub(f'{word}', f'<say-as interpret-as="characters">{word}</say-as>', data)
                    words.append(word)
            except Exception:
                pass

            fp.write('<speak>\n')

            for line in data.splitlines():
                line = '<s>' + line + '</s>' + '\n'
                fp.write(line)

            fp.write('</speak>')

        print(f'Article {[num]} : Summarized & Saved')
        num += 1
        time.sleep(3)

os.chdir(f'..')

# log file generation for all the articles scraped
csv_columns = ['Title', 'Link', 'Published Date']
log = f'log.csv'
with open(log, 'w') as f:
    writer = csv.DictWriter(f, fieldnames=csv_columns)
    writer.writeheader()
    for data in feed_list:
        writer.writerow(data)


print(f'\n\nTotal {num - 1 - error}  articles summarized and saved in {os.getcwd()}')
print(f'Logged each article with its information in {log}')
