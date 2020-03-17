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

    tkinter = Tkinter  # I decided to use a library reference to avoid potential naming conflicts with people's programs.
else:
    import tkinter

root = tkinter.Tk()
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()

pg.init()
ua = UserAgent(
    fallback='Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11')
url = 'https://www.reddit.com/r/cats.json?limit=10000'
response = requests.get(url, headers={'User-agent': ua.random})

if not response.ok:
    print("Error", response.status_code)
    exit()
data = response.json()['data']['children']

clock = pg.time.Clock()


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
    # image = pg.transform.scale(image, findsize(image.get_size()))
    print(image.get_size())
    print(findsize(image.get_size()))
    image = pg.transform.scale(image, findsize(image.get_size()))
    rect = image.get_rect()
    rect = rect.move(((1920/2) - (image.get_size()[0]/2), 0))

    screen.blit(image, rect)
    pg.display.update()
    time.sleep(2)

def findsize(size):
    # if (size[1] >= size[0]):
    delta = 1080/size[1]
    width = int(round(size[0]*delta))
    height = int(round(size[1]*delta))
    # print("first")
    return width, height
    # # else:
    #     delta = 1920 / size[0]
    #     width = int(round(size[0] * delta))
    #     height = int(round(size[1] * delta))
    #     # print("first")
    #     return width, height


while True:
    for i in range(len(data)):
        current_post = data[i]['data']
        image_url = current_post['url']
        image = requests.get(image_url, allow_redirects=False)
        if (image.status_code == 200):
            try:
                show_image(image_url)
            except:
                pass
