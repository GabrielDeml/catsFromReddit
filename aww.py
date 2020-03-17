# These was super useful:
# https://medium.com/@naveenkumarspa/using-python-for-your-desktop-wallpaper-collection-focused-on-beginners-a66451d25660
# https://www.daniweb.com/programming/software-development/code/493004/display-an-image-from-the-web-pygame
import sys
import io
import pygame as pg
import requests
from fake_useragent import UserAgent
import time

try:
    # Python2
    from urllib2 import urlopen
except ImportError:
    # Python3
    from urllib.request import urlopen

if sys.version_info[0] == 2:  # the tkinter library changed it's name from Python 2 to 3.
    import Tkinter
    tkinter = Tkinter #I decided to use a library reference to avoid potential naming conflicts with people's programs.
else:
    import tkinter

root = tkinter.Tk()
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()

pg.init()
ua = UserAgent(
    fallback='Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11')
url = 'https://www.reddit.com/r/aww.json?limit=100'
response = requests.get(url, headers={'User-agent': ua.random})

if not response.ok:
    print("Error", response.status_code)
    exit()
data = response.json()['data']['children']

def show_image(image_url):
    image_str = urlopen(image_url).read()
    # create a file object (stream)
    image_file = io.BytesIO(image_str)
    print(image_file)
    # (r, g, b) color tuple, values 0 to 255
    black = (0, 0, 0)
    # create a 600x400 black screen
    screen = pg.display.set_mode((screen_width, screen_height), pg.RESIZABLE)
    screen.fill(black)
    # load the image from a file or stream
    image = pg.image.load(image_file)
    rect = image.get_rect()
    # image = pg.transform(image, (screen_width, screen_height))
    # draw image, position the image ulc at x=20, y=20
    screen.blit(image, (0, 0))
    # nothing gets displayed until one updates the screen
    pg.display.flip()
    time.sleep(1)


for i in range(len(data)):
    current_post = data[i]['data']
    image_url = current_post['url']
    # if '.png' in image_url:
    #     extension = '.png'
    # elif '.jpg' in image_url or '.jpeg' in image_url:
    #     extension = '.jpeg'
    # elif 'imgur' in image_url:
    #     image_url += '.jpeg'
    #     extension = '.jpeg'
    # else:
    #     continue
    image = requests.get(image_url, allow_redirects=False)
    if (image.status_code == 200):
        try:
            # output_filehandle = open(current_post['title'] + extension, mode='bx')
            # output_filehandle.write(image.content)
            show_image(image_url)
        except:
            pass



