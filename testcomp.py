import random
import urllib
import sys
import os
import json
from bs4 import BeautifulSoup
import requests
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, vfx
from moviepy.video.fx.resize import resize
from PIL import Image, ImageDraw, ImageFont

fname = sys.argv[1]

clip = VideoFileClip(fname)
# clip.write_gif('t0.gif', fps=15, loop=1)
# clip.speedx(1.8).write_gif('t1.gif', fps=7, loop=1)
# clip.speedx(1.8).write_gif('t2.gif', fps=5, loop=1)
# clip.speedx(2.4).write_gif('t3.gif', fps=4, loop=1)
# clip.speedx(2.3).write_gif('t4.gif', fps=4, loop=1)
# clip.speedx(2.2).write_gif('t5.gif', fps=4, loop=1)
# clip.speedx(2.1).write_gif('t6.gif', fps=4, loop=1)
# clip.speedx(2.4).write_gif('t7.gif', fps=5, loop=1)
clip.resize(.8)
clip.speedx(1.8).write_gif('t8.gif', fps=7, loop=1)
# clip.speedx(1.8).write_gif('t4.gif', fps=5, loop=1, opt='wu')
# clip.speedx(1.7).write_gif('t2.gif', fps=7, loop=1, opt='wu')
# clip.speedx(1.7).write_gif('t3.gif', fps=7, loop=1, program='ffmpeg')
# clip.speedx(1.7).write_gif('t4.gif', fps=7, loop=1, program='ImageMagick', opt='optimizeplus', fuzz=10)
