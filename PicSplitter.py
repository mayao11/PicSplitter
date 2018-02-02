import os, sys
from PIL import Image

def SplitPic(img, w, h):
    l = []
    width,height = img.size
    for y in range(0,height,h):
        for x in range(0,width,w):
            if (x+w-width)/w > 0.5 or (y+h-height)/h > 0.5:
                continue
            box = (x,y,x+w,y+h)
            small_im = img.crop(box)
            print(small_im, x, y, x+w, y+h)
            l.append(small_im)
    return l

def SavePics(path, l):
    file_name = os.path.basename(path).split(".")[0]
    for i in range(len(l)):
        img = l[i]
        img.save("%s_%s.png"%(file_name, (i+1)), 'png')
    return


def LoadImage(path):
    img = Image.open(path)
    return img


if __name__ == "__main__":
    img_path = sys.argv[1]
    w = int(sys.argv[2])
    h = int(sys.argv[3])
    img = LoadImage(img_path)
    l = SplitPic(img, w, h)
    pics = SavePics(img_path, l)

