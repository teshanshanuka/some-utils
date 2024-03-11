#!/usr/bin/python3
# Author: Teshan Liyanage <teshanuka@gmail.com>

"""Images to pdf"""

import sys

if len(sys.argv) < 3:
    print("Usage ./script <img1.png> [<img2.png> ...] <output.pdf>")
    sys.exit(1)

from PIL import Image

# For `OSError: image file is truncated`
# from PIL import ImageFile
# ImageFile.LOAD_TRUNCATED_IMAGES = True

imgs = sys.argv[1:-1]
op = sys.argv[-1]

img1, *imgsN = [Image.open(img) for img in imgs]
img1.save(op, "PDF" ,resolution=100.0, save_all=True, append_images=imgsN)
