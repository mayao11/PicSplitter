import re
from PIL import Image, ImageTk, ImageChops
import tkinter as tk
from tkinter import messagebox
from TkinterDnD2 import *

root = TkinterDnD.Tk()

gSelectedImageIndex = -1
gBackImageIndex = tk.IntVar()
gBackImageIndex.set(-1)
gLblImage = None
gBigPhotoImage = None
gImageSizeVarX = tk.StringVar()
gImageSizeVarY = tk.StringVar()
gImageSizeEntryX = None
gImageSizeEntryY = None


def isolate_name(s):
    t = s.split('.')
    name = t[-2]
    it = re.finditer(r'\d+', name)
    match = list(it)[-1]
    num = match.group()
    if len(num) < 4:
        num = "0"*(4-len(num)) + num
    ret = s[:match.start()] + num + s[match.end():]
    return ret


class ImageFile(object):
    def __init__(self, file_name):
        self.image = Image.open(file_name)
        self.fileName = file_name
        self.isolateFileName = isolate_name(self.fileName)
        self.order = 0

        self.label = None
        self.photoImage = None
        self.frame = None
        self.bigImage = None

        self.offsetX = 0
        self.offsetY = 0


class FusionImage(object):
    def __init__(self):
        self.image = None
        self.photoImage = None
        self.label = None


images = []


def show_images():
    def _on_image_click(index):
        def func(evt):
            return on_image_click(evt, index)
        return func

    def _on_radiobutton_click(index):
        def func():
            return on_radiobutton_click(index)
        return func

    for i, imageFile in enumerate(images):
        img_temp = imageFile.image.copy()
        img_temp.thumbnail((100, 100))
        img = ImageTk.PhotoImage(img_temp)

        frame = tk.Frame(root)
        lbl = tk.Label(frame, image=img)
        lbl.pack()
        radio = tk.Radiobutton(frame, variable=gBackImageIndex, value=i, command=_on_radiobutton_click(i))
        radio.pack()

        lbl.bind("<Button-1>", _on_image_click(i))

        imageFile.label = lbl
        imageFile.photoImage = img
        imageFile.frame = frame
        frame.pack(side=tk.LEFT)
    refresh_image_activate()
    return


def refresh_image_activate():
    global gSelectedImageIndex
    for i, image_file in enumerate(images):
        if i != gSelectedImageIndex:
            image_file.label.config(bg="lightgrey")
        else:
            image_file.label.config(bg="blue")
    return


def on_image_click(event, index):
    global gSelectedImageIndex
    gSelectedImageIndex = index
    refresh_image_activate()
    move_image(0, 0)


def on_radiobutton_click(index):
    global gSelectedImageIndex
    if gSelectedImageIndex == -1:
        gSelectedImageIndex = index
        refresh_image_activate()
    move_image(0, 0)


def clear_images():
    for i, imageFile in enumerate(images):
        imageFile.frame.destroy()


def on_file_drop(event):
    files = event.data.split()
    clear_images()
    for name in files:
        exist = False
        for image_file in images:
            if image_file.fileName == name:
                exist = True
                break
        if not exist:
            image_file = ImageFile(name)
            images.append(image_file)
    images.sort(key=lambda im: im.isolateFileName)
    for image_file in images:
        print(image_file.fileName)
        expand_global_size(image_file.image.size)
    show_images()


def move_image(ox, oy):
    global gBigPhotoImage
    print("MoveImage", gBackImageIndex.get())
    if gSelectedImageIndex == -1:
        return

    back = None
    if gBackImageIndex.get() != -1 and gBackImageIndex.get() != gSelectedImageIndex:
        back_file = images[gBackImageIndex.get()]
        if back_file.bigImage is None:
            back_file.bigImage = Image.open(back_file.fileName)
            back_file.bigImage = expand_image(back_file.bigImage)
        back = back_file.bigImage
        back = ImageChops.offset(back, back_file.offsetX, back_file.offsetY)

    image_file = images[gSelectedImageIndex]
    image_file.offsetX += ox
    image_file.offsetY += oy
    if image_file.bigImage is None:
        image_file.bigImage = Image.open(image_file.fileName)
    image_file.bigImage = expand_image(image_file.bigImage)
    temp = image_file.bigImage
    temp = ImageChops.offset(temp, image_file.offsetX, image_file.offsetY)

    if back is not None:
        temp = ImageChops.blend(temp, back, 0.5)

    img = ImageTk.PhotoImage(temp)
    gBigPhotoImage = img

    gLblImage.config(image=img)

    return


def expand_image(image):
    if not need_expand_image(image):
        return image
    new_image = Image.new(image.mode, global_size())
    cur = image.size
    new_image.paste(image, ((new_image.size[0]-cur[0])/2, (new_image.size[1]-cur[1])/2))
    return new_image


def global_size():
    try:
        x = int(gImageSizeVarX.get())
        y = int(gImageSizeVarY.get())
    except ValueError:
        x, y = 0, 0
    ret = [x, y]
    return tuple(ret)


def expand_global_size(t):
    cur = global_size()
    gImageSizeVarX.set(max(t[0], cur[0]))
    gImageSizeVarY.set(max(t[1], cur[1]))


def need_expand_image(image):
    cur = global_size()
    return image.size[0] < cur[0] or image.size[1] < cur[1]


def on_save_all_click():
    if not messagebox.askokcancel("全部保存", '保存文件会直接修改所有文件，是否继续？'):
        return
    for i, image_file in enumerate(images):
        if image_file.bigImage is not None:
            temp = image_file.bigImage
            temp = ImageChops.offset(temp, image_file.offsetX, image_file.offsetY)
            temp.save(image_file.fileName)
            print("覆盖保存了", image_file.fileName)


def start():
    global gLblImage, gImageSizeEntryX, gImageSizeEntryY
    root.bind("<Up>", lambda evt: move_image(0, -1))
    root.bind("<Down>", lambda evt: move_image(0, 1))
    root.bind("<Left>", lambda evt: move_image(-1, 0))
    root.bind("<Right>", lambda evt: move_image(1, 0))
    lbl_drag = tk.Label(root, text="将切好的图片拖到这里，名称要有序且不包含空格")
    lbl_drag.drop_target_register(DND_FILES)
    lbl_drag.dnd_bind('<<Drop>>', on_file_drop)

    gLblImage = tk.Label(root, text="...")

    lbl_drag.pack(expand=1)

    def _test_digit(content):
        return content == "" or content.isdigit()

    test_cmd = root.register(_test_digit)
    gImageSizeEntryX = tk.Entry(root, textvariable=gImageSizeVarX, validate='key', validatecommand=(test_cmd, '%P'))
    gImageSizeEntryY = tk.Entry(root, textvariable=gImageSizeVarY, validate='key', validatecommand=(test_cmd, '%P'))
    gImageSizeEntryX.pack()
    gImageSizeEntryY.pack()

    tk.Button(root, text='全部保存', command=on_save_all_click).pack()

    gLblImage.pack()
    root.mainloop()


if __name__ == '__main__':
    start()
