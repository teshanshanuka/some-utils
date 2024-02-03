#!/usr/bin/python3
# Author: Teshan Liyanage <teshanuka@gmail.com>

import sys
from PyPDF2 import PdfMerger

"""Create a new pdf from a subset of pages from the original"""

if len(sys.argv) < 4:
    print("Usage ./script <input1.pdf> <input2.pdf> [<input3.pdf> ...] <output.pdf>")
    sys.exit(1)

pdfs = sys.argv[1:-1]
op = sys.argv[-1]

print(f"Creating {op} from {','.join(pdfs)}")

merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write(op)
merger.close()
