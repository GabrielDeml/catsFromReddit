# These was super useful:
# https://medium.com/@naveenkumarspa/using-python-for-your-desktop-wallpaper-collection-focused-on-beginners-a66451d25660
# https://www.daniweb.com/programming/software-development/code/493004/display-an-image-from-the-web-pygame
# https://stackoverflow.com/questions/47316266/can-i-display-image-in-full-screen-mode-with-pil
import sys
import io
# import pygame as pg
import requests
import time
from PIL.Image import Image
from PIL import Image, ImageTk
from fake_useragent import UserAgent
from io import BytesIO


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

# pg.init()
ua = UserAgent(
    fallback='Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11')
url = 'https://www.reddit.com/r/aww.json?limit=100'
response = requests.get(url, headers={'User-agent': ua.random})

if not response.ok:
    print("Error", response.status_code)
    exit()
data = response.json()['data']['children']

def show_image(image):
    print("hello from show_image")

    pilImage = Image.open(BytesIO(image.content))
    # pilImage.show()
    showPIL(pilImage)
    time.sleep(1)

def showPIL(pilImage):
    root = tkinter.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()
    root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
    canvas = tkinter.Canvas(root,width=w,height=h)
    canvas.pack()
    canvas.configure(background='black')
    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w/imgWidth, h/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w/2,h/2,image=image)
    root.mainloop()



for i in range(len(data)):
    current_post = data[i]['data']
    image_url = current_post['url']
    if '.png' in image_url:
        extension = '.png'
    elif '.jpg' in image_url or '.jpeg' in image_url:
        extension = '.jpeg'
    elif 'imgur' in image_url:
        image_url += '.jpeg'
        extension = '.jpeg'
    else:
        continue
    image = requests.get(image_url, allow_redirects=False)
    print("hello from loop: " + str(i) + str(image.status_code))
    if (image.status_code == 200):
        try:
            print("trying to show image")
            # output_filehandle = open(current_post['title'] + extension, mode='bx')
            # output_filehandle.write(image.content)
            show_image(image)

        except:
            pass



