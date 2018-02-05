import os, sys
from PIL import Image

def DiffScore(img1, img2):
    l = [1 for i in range(len(img1.getdata())) if img1.getdata()[i] != img2.getdata()[i]]
    return sum(l)

def IsEmptyImage(img):
    d = img.getdata()
    l = [1 for i in range(len(d)-1) if d[i+1] != d[i]]
    threshold = img.size[0] * img.size[1] / 50
    s = sum(l)
    print("sum:", s, "threshold", threshold)
    return s < threshold

def FindBestFit(img, last_small_img, x, y, w, h):
    best_score = 99999999;
    best_box = None
    offset_x = int(w * 0.05) or 1
    offset_y = int(h * 0.05) or 1
    print(x, y, offset_x, offset_y)
    for ox in range(-offset_x, offset_x+1):
        for oy in range(-offset_y, offset_y+1):
            box = (x+ox, y+oy, x+ox+w, y+oy+h)
            small_img = img.crop(box)
            if last_small_img != None:
                score = DiffScore(small_img, last_small_img)
                if best_score > score:
                    best_score = score
                    best_box = box
    best_img = img.crop(best_box)
    return best_img


def SplitPic(img, w, h):
    l = []
    width,height = img.size
    last_small_img = None
    for y in range(0,height,h):
        for x in range(0,width,w):
            if (x+w-width)/w > 0.5 or (y+h-height)/h > 0.5:
                continue
            box = (x, y, x+w, y+h)
            small_img = img.crop(box)
            if IsEmptyImage(small_img):
                print("Empty", x, y)
                continue;
            if last_small_img != None:
                small_img = FindBestFit(img, last_small_img, x, y, w, h)
            last_small_img = small_img

            print("----", x, y, x+w, y+h)
            l.append(small_img)
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


