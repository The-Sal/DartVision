#  Copyright (c) 2023. THE FOLLOWING CODE IS NOT TO BE USED WITHOUT PERMISSION FROM THE AUTHOR.
#  THE FOLLOWING CODE WAS WRITTEN FOR EDUCATIONAL PURPOSES.
#  Author: Sal Faris
#  Email: hz14n7os@duck.com
#  Github: github.com/The-Sal
import os
import subprocess
import tempfile
from Vis._util import *
from utils3 import base64DecodeFile, assertTypes

_anyType = type(None)

class _BinaryDecompression:
    """A Super Class which gives access to the OCR binary"""
    def __init__(self, binary_module):
        self._binary_module = binary_module
        self._pth = None
        self._temp = None
        self._deleted = False



    # Make sure to clean up any instances of this class
    def __del__(self):
        if self._pth is not None:
            os.remove(self._pth)
            self._temp.close()
        self._deleted = True


    def _decompress(self):
        try:
            assert hasattr(self._binary_module, 'binary')
        except AssertionError:
            raise PythonBinaryError('Cannot find binary attribute in module')

        temp_file = tempfile.NamedTemporaryFile(delete=False)
        binary = self._binary_module.binary
        file_binary = base64DecodeFile(
            file_path=temp_file.name,
            data=binary
        )

        self._temp = temp_file

        return temp_file.name

    def _make_binary_executable(self):
        os.chmod(self._pth, 0o777)


    @property
    def ocr_binary(self):
        assert self._deleted is False, 'This instance has been deleted'
        if self._pth is None:
            self._pth = self._decompress()
            self._make_binary_executable()

        return self._pth


class OCRBinaryError(VisionError):
    pass


class OCR(_BinaryDecompression):
    """A class to interact with DartVision's OCR APIs. This class is re-usable, and
    it's best practice to create a single instance of this class and use it for all the OCR
    operations you need to perform. Call close() when you are done with the instance."""
    def __init__(self):
        try:
            from Vis import _ocr as binary_module
            super().__init__(binary_module)
        except ImportError:
            raise PythonBinaryError('Cannot find binary module')

    def recognize(self, image: str) -> [str]:
        """Recognize text from an image"""
        binary = self.ocr_binary
        proc = subprocess.Popen(
            [
                binary,
                image
            ],
            stdout=subprocess.PIPE
        )

        out, err = proc.communicate()
        if err is not None:
            raise OCRBinaryError(err)

        # The output is something like this: ["hello", "old", "friend"]
        # We need to remove the quotes and the brackets
        out = out.decode('utf-8')
        out = out.replace('"', '')
        out = out.replace('[', '')
        out = out.replace(']', '')
        out = out.split(',')
        for i, item in enumerate(out):
            out[i] = item.strip()

        return out


    def close(self):
        """Close the instance of this class. This is best practice to do when you are done
        using the instance of this class."""
        del self


if __name__ == '__main__':
    ocr = OCR()
    with ScreenShot() as ss:
        print(ocr.recognize(ss))
    ocr.close()
