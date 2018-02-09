import os, sys
from PIL import Image
from PIL import ImageChops

img1 = Image.open("syokuzi_ie_1.png")
img2 = Image.open("syokuzi_ie_6.png")


img = ImageChops.blend(img1, img2, 0.5)
print(img)
img.show()

