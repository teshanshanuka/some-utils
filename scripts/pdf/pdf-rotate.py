#!/usr/bin/python3
# Author: Teshan Liyanage <teshanuka@gmail.com>

import sys
from PyPDF2 import PdfWriter, PdfReader

"""Rotate a subset of pages from the original"""

if len(sys.argv) < 5:
    print("Usage ./script <input.pdf> <pg1> <rot1> [<pg2> <rot2>...] <output.pdf>")
    sys.exit(1)

ip = sys.argv[1]
pages = list(map(int, sys.argv[2:-2:2]))
rots = list(map(float, sys.argv[3:-1:2]))
op = sys.argv[-1]

if len(pages) != len(rots):
    print("Number of pages and rotations must be equal")
    sys.exit(1)

op = sys.argv[-1]

print(f"Creating '{op}' from '{ip}' pages {pages}, with rotations {rots}")


with open(ip, "rb") as ifd, open(op, "wb") as ofd:
    inputpdf = PdfReader(ifd)
    output = PdfWriter()

    for i, page in enumerate(inputpdf.pages):
        try:
            idx = pages.index(i+1)
            page.rotate(rots[idx])
        except ValueError:
            pass
        output.add_page(page)

    output.write(ofd)
