#!/usr/bin/python3
# Author: Teshan Liyanage <teshanuka@gmail.com>

import sys
from PyPDF2 import PdfFileWriter, PdfFileReader

"""Create a new pdf from a subset of pages from the original"""

if len(sys.argv) < 4:
    print("Usage ./script <input.pdf> <pg1> [<pg2> ...] <output.pdf>")
    sys.exit(1)

ip = sys.argv[1]
pages = list(map(int, sys.argv[2:-1]))
op = sys.argv[-1]

print(f"Creating '{op}' from pages {pages}")


with open(ip, "rb") as ifd, open(op, "wb") as ofd:
    inputpdf = PdfFileReader(ifd)
    output = PdfFileWriter()

    for i in range(inputpdf.numPages):
        if i+1 in pages:
            output.addPage(inputpdf.getPage(i))

    output.write(ofd)
