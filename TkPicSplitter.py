import re
from PIL import Image, ImageTk, ImageChops
import tkinter as tk
from TkinterDnD2 import *

root = TkinterDnD.Tk()

#textRows = tk.StringVar()
#textRows.set("1")

selectedImageIndex = -1
lblImage = None

def IsolateName(s):
    l = s.split('.')
    name = l[-2]
    it = re.finditer(r'\d+', name)
    match = list(it)[-1]
    num = match.group()
    if len(num) < 4:
        num = "0"*(4-len(num)) + num
    ret = s[:match.start()] + num + s[match.end():]
    return ret

class ImageFile(object):
    def __init__(self, fileName):
        self.image = Image.open(fileName)
        self.fileName = fileName
        self.isolateFileName = IsolateName(self.fileName)
        self.checkValue = tk.IntVar()
        self.order = 0

        self.label = None
        self.photoImage = None
        self.frame = None
        self.checkbutton = None
        self.bigImage = None

        self.offsetX = 0
        self.offsetY = 0

class FusionImage(object):
    def __init__(self):
        self.image = None
        self.photoImage = None
        self.label = None

images = []

def ShowImages():
    def _OnCheckbutton(i):
        def func():
            return OnCheckbutton(i)
        return func
    def _OnImageClick(i):
        def func(evt):
            return OnImageClick(evt, i)
        return func
    for i, imageFile in enumerate(images):
        imgTemp = imageFile.image.copy()
        imgTemp.thumbnail((100,100))
        img = ImageTk.PhotoImage(imgTemp)

        frame = tk.Frame(root)
        lbl = tk.Label(frame, image=img)
        checkbutton = tk.Checkbutton(frame, variable=imageFile.checkValue, command=_OnCheckbutton(i))
        lbl.pack()
        checkbutton.pack()

        lbl.bind("<Button-1>", _OnImageClick(i))

        imageFile.label = lbl
        imageFile.photoImage = img
        imageFile.frame = frame
        imageFile.checkbutton = checkbutton
        frame.pack(side=tk.LEFT)

def OnImageClick(event, index):
    global selectedImageIndex
    print("OnImageClick", event, index)
    selectedImageIndex = index


def ClearImages():
    for i, imageFile in enumerate(images):
        imageFile.frame.destroy()

def OnFileDrop(event):
    files = event.data.split()
    ClearImages()
    for name in files:
        exist = False
        for imageFile in images:
            if imageFile.fileName == name:
                exist = True
                break
        if not exist:
            imageFile = ImageFile(name)
            images.append(imageFile)
    images.sort(key=lambda im:im.isolateFileName)
    for imageFile in images:
        print(imageFile.fileName)
    ShowImages()


def OnCheckbutton(index):
    print("OnCheckbutton", index)

def MoveImage(ox, oy):
    if selectedImageIndex == -1:
        return
    imageFile = images[selectedImageIndex]
    imageFile.offsetX += ox
    imageFile.offsetY += oy
    temp = Image.open(imageFile.fileName)
    temp = ImageChops.offset(temp, imageFile.offsetX, imageFile.offsetY)
    img = ImageTk.PhotoImage(temp)
    imageFile.bigImage = img
    lblImage.config(image = img)
    return

def Start():
    global lblImage
    root.bind("<Up>", lambda evt:MoveImage(0, -1))
    root.bind("<Down>", lambda evt:MoveImage(0, 1))
    root.bind("<Left>", lambda evt:MoveImage(-1, 0))
    root.bind("<Right>", lambda evt:MoveImage(1, 0))
    lblDrag = tk.Label(root, text="将切好的图片拖到这里。（文件名不支持空格）")
    lblDrag.drop_target_register(DND_FILES)
    lblDrag.dnd_bind('<<Drop>>', OnFileDrop)

    lblImage = tk.Label(root, text="...")

    lblDrag.pack(expand=1)
    lblImage.pack()
    root.mainloop()

if __name__ == '__main__':
    Start()

