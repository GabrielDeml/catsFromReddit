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
    import Tkinter

    tkinter = Tkinter
except ImportError:
    # Python3
    from urllib.request import urlopen
    import tkinter

# Change me to your screen resolution
screen_width = 1920
screen_height = 1080

# Change this to change how long to display the image
timeToWait = 2

# In it pygame
pg.init()
clock = pg.time.Clock()

# Get user agent and stuff
ua = UserAgent(
    fallback='Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11')

# Reddit url to get images and how many to get
# Change limit if you want more
url = ['https://www.reddit.com/r/cats.json?limit=10000', 'https://www.reddit.com/r/aww.json?limit=10000']



def show_image(inputImage):
    # create a file object (stream)
    image_file = io.BytesIO(inputImage)
    # (r, g, b) color tuple, values 0 to 255
    black = (0, 0, 0)
    # create a 600x400 black screen
    screen = pg.display.set_mode((screen_width, screen_height), pg.RESIZABLE)
    screen.fill(black)
    # load the image from a file or stream
    image = pg.image.load(image_file)
    # Scale the image
    image = pg.transform.scale(image, findsize(image.get_size()))
    # Move the image to the center of the screen
    rect = image.get_rect()
    rect = rect.move(((screen_width / 2) - (image.get_size()[0] / 2), 0))
    screen.blit(image, rect)
    # Display the image
    pg.display.update()
    # Wait for time
    time.sleep(timeToWait)


def findsize(size):
    delta = screen_height / size[1]
    width = int(round(size[0] * delta))
    height = int(round(size[1] * delta))
    return width, height


# Forever get the images
while True:
    for n in range(len(url)):
        response = requests.get(url[n], headers={'User-agent': ua.random})

        # Make sure we got a good response
        if not response.ok:
            print("Error", response.status_code)
            exit()
        data = response.json()['data']['children']
        for i in range(len(data)):
            current_post = data[i]['data']
            image_url = current_post['url']
            image = requests.get(image_url, allow_redirects=False)
            if image.status_code == 200:
                try:
                    show_image(image.content)
                except:
                    pass
