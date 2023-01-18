#  Copyright (c) 2023. THE FOLLOWING CODE IS NOT TO BE USED WITHOUT PERMISSION FROM THE AUTHOR.
#  THE FOLLOWING CODE WAS WRITTEN FOR EDUCATIONAL PURPOSES.
#  Author: Sal Faris
#  Email: hz14n7os@duck.com
#  Github: github.com/The-Sal
import subprocess

# Private File. Do not import!
# This file is used to convert our OCR binary into data that can be used to create a python-representation of the
# binary. This is done via the BinToPy Executable written for MusicGrabber.

from utils3 import base64File
from importlib import import_module
file = base64File('binary/OCR')
with open('_ocr.py', 'w+') as f:
    f.write('# OCR Binary\n# Generated by _ocr_loading.py\n')
    f.write('binary = "{}"'.format(file.decode()))

ocr = import_module('_ocr')
assert hasattr(ocr, 'binary'), 'Unable to import binary'


