import argparse
import json
import itertools
# import re
# import os
# import uuid
# import sys
from urllib.request import urlopen, Request
from subprocess import call
from bs4 import BeautifulSoup


REQUEST_HEADER = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}


def get_soup(url, header):
    response = urlopen(Request(url, headers=header))
    return BeautifulSoup(response, 'html.parser')


def get_query_url(query):
    return "https://www.google.com/search?q=%s&source=lnms&tbm=isch&tbs=itp:photo" % query


def extract_images_from_soup(soup):
    image_elements = soup.find_all("div", {"class": "rg_meta"})
    metadata_dicts = (json.loads(e.text) for e in image_elements)
    link_type_records = []
    for d in metadata_dicts:
        # images must be either jpg or png and larger than 700x470
        if (d['oh'] < 470 or d['ow'] < 700) or (d['ou'][-4:] != '.jpg' and d['ou'][-4:] != '.png'):
            continue
        link_type_records.append(d["ou"])
    return link_type_records


def extract_images(query, num_images):
    url = get_query_url(query)
    soup = get_soup(url, REQUEST_HEADER)
    link_type_records = extract_images_from_soup(soup)
    return itertools.islice(link_type_records, num_images)


def save_image(url, save_directory):
    try:
        call(f'wget -t 1 {url} -P "{save_directory}"', shell=True)
        # print(f'{save_directory}\n{url}\n{num}.{ext}')
    except Exception as e:
        print(e)


def download_images_to_dir(images, save_directory):
    num = 1
    for url in images:
        try:
            # raw_image = get_raw_image(url)
            save_image(url, save_directory)
            # print(url)
        except Exception as e:
            print(e)


def run(query, save_directory, num_images=100):
    query = '+'.join(query.split())
    # logger.info("Extracting image links")
    images = extract_images(query, num_images)
    # logger.info("Downloading images")
    download_images_to_dir(images, save_directory)
    # logger.info("Finished")


def main():
    parser = argparse.ArgumentParser(description='Scrape Google images')
    parser.add_argument('-s', '--search', default='bananas', type=str, help='search term')
    parser.add_argument('-n', '--num_images', default=1, type=int, help='num images to save')
    parser.add_argument('-d', '--directory', default='/home/sr1/googleImages/extractImages', type=str, help='save directory')
    args = parser.parse_args()
    run(args.search, args.directory, args.num_images)


if __name__ == '__main__':
    main()
