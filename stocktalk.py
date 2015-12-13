import random
import urllib
import sys
import os
import json
from bs4 import BeautifulSoup
import requests
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont


def download_file(url, keyword=''):
    print 'downloading', url
    local_filename = 'footage/' + keyword + url.split('/')[-1]
    if os.path.exists(local_filename):
        return local_filename
    # urllib.urlretrieve(url, local_filename)
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename


def get_shutterstock_vids(q, total=1):
    search_url = 'http://www.shutterstock.com/video/search/?site=videos&version=llv1&searchterm='
    base_url = 'http://www.shutterstock.com'
    r = requests.get(search_url + q)
    soup = BeautifulSoup(r.text, "html.parser")

    downloads = []
    links = [l.get('href') for l in soup.select('.clip-item a.clip')]

    if len(links) == 0:
        return None

    random.shuffle(links)

    for l in links[0:total]:
        r = requests.get(base_url + l)
        soup = BeautifulSoup(r.text, "html.parser")
        vid = soup.select('video source')[0].get('src')
        filename = download_file(vid)
        downloads.append(filename)

    if total == 1:
        downloads = downloads[0]

    return downloads


def create_sub(text, size, fntname='/Library/Fonts/Arial Bold.ttf', padding=0.02, bg=(0, 0, 0, 230), fg=(255, 255, 255), rect_offset=None, min_height=85):

    padding = size[0] * padding

    img = Image.new('RGBA', size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    fontsize = 200
    fnt = ImageFont.truetype(fntname, fontsize)
    textsize = fnt.getsize(text)

    while textsize[0]+padding > size[0] or textsize[1]+padding > size[1]:
        fontsize -= 1
        fnt = ImageFont.truetype(fntname, fontsize)
        textsize = fnt.getsize(text)

    offset = fnt.getoffset(text)
    text_width = textsize[0]
    text_height = textsize[1] + offset[1]

    # incredibly dumb hack to get the proper height
    # text_height = fnt.getsize('y' + text[1:])[1]

    # x = size[0]/2.0 - textsize[0]/2.0
    # y = size[1]/2.0 - textsize[1]/2.0
    x = (size[0] - text_width) / 2.0
    y = (size[1] - text_height) / 2.0

    rect_h = max(text_height + padding, min_height)
    rect_y = (size[1] - rect_h) / 2.0

    if rect_offset is not None:
        y = rect_offset + (rect_h - text_height)/2.0
        rect_y = rect_offset

    d.rectangle([0, rect_y, size[0], rect_y+rect_h], fill=bg)
    d.text((x, y), text, font=fnt, fill=fg)

    imgfile = 'images/' + text + '.png'
    img.save(imgfile, 'PNG')

    clip = ImageClip(imgfile.encode('ascii'))
    return clip


def save_out(tracks, outfile=None):

    out = []

    vids = [t for t in tracks if t['type'] == 'vid']
    texts = [t for t in tracks if t['type'] == 'text']

    for v in vids:
        c = VideoFileClip(v['content']).subclip(v['in'], v['in'] + v['duration'])
        c = c.set_start(v['start'])
        out.append(c)

    size = out[0].size

    for t in texts:
        c = create_sub(t['content'], size, rect_offset=195, min_height=55)
        c = c.set_start(t['start'])
        c = c.set_duration(t['duration'])
        out.append(c)

    final_clip = CompositeVideoClip(out)
    if outfile is None:
        outfile = 'ad_' + str(int(time.time())) + '.mp4'
    final_clip.write_videofile(outfile, fps=24)
    return outfile


def compose(parts):
    out = []
    t = 0

    for p in parts:
        vid = get_shutterstock_vids(p['query'])

        duration = random.uniform(4, 5)
        # text = 'You ' + p['verb'] + ' ' + p['text']
        text = p['text']
        text = text.upper()

        vidtrack = {'type': 'vid', 'content': vid, 'start': t, 'duration': duration, 'in': 0}
        texttrack = {'type': 'text', 'content': text, 'start': t, 'duration': duration}

        out.append(vidtrack)
        out.append(texttrack)

        t += duration

    return out

if __name__ == '__main__':
    parts = [
        {'query': 'eternity', 'text': 'Hello amelia'},
        {'query': 'meat', 'text': 'Hope you are doing ok'},
        {'query': 'eroticism', 'text': 'Get better soon'},
    ]

    composition = compose(parts)
    final = save_out(composition)
