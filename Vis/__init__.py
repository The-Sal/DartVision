"""Dart Vision Library"""
import cv2
from utils2 import system  # install with pip from github.com/the-sal/utils2 using 'git+' prefix
def __guaranteeImport(module):
    """This function is used to guarantee that a module is imported from within
    the library. This makes it easier to write code/test the library without having
    repeatedly using try/except blocks to import modules"""
    try:
        # when stand-alone run, this will work
        mod = __import__(module)
    except ImportError:
        # When imported as a library, this will work
        mod = __import__('.{}'.format(module), fromlist=['*'])  # act as from . import module

    return mod

_util = __guaranteeImport('_util')


class ImageCords:
    """Image Cords
    This class is used to find the location of an image on the screen."""

    def __init__(self, image):
        self._image = cv2.imread(image)
        self._cords = None

    def _find_image(self):
        screen_shot = _util.ScreenShot()
        with screen_shot as ss:
            screen = cv2.imread(ss)
            result = cv2.matchTemplate(screen, self._image, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # We need a multiplier to map the coordinates to the screen size
            # this is because coordinates are based on the image size
            # and the screen size can be different
            # On tested MacBookAir 13" the screen size is 1440x900
            # and the image size is 2880x1800
            # so what we did is ge the value from cv2 and compare it to the value
            # we get when using ctrl+shit+4 and then divide the actual value by the
            # value we get from cv2, this gives us a multiplier
            # we then multiply the cv2 value by the multiplier to get the actual value
            # this is not the best way to do it, but it works
            # (only tested on MacBookAir 13")
            # Ideally the multiplier should be calculated dynamically,
            # but I don't know how to do that yet so I'm just using a static value.


            multiplier = 0.50472069236
            self._cords = ((max_loc[0] * multiplier).__int__(), (max_loc[1] * multiplier).__int__())
            self._cords = (self._cords[0] + 1, self._cords[1] + 1)



    @property
    def cords(self):
        if self._cords is None:
            self._find_image()
        return self._cords


if __name__ == '__main__':
    def _click(x, y):
        # DO NOT USE THIS FUNCTION, it is only for testing
        x = str(x)
        y = str(y)
        # VM path to cliclick
        clicker = '/Users/Sal/.Dart2-Install/cliclick'
        system.command([clicker, 'c:' + x + ',' + y], waitUntilFinished=True)

    def _tester(sample_img):
        # DO NOT USE THIS FUNCTION, it is only for testing
        img = ImageCords(sample_img)
        print('Found image {} at: {}'.format(sample_img, img.cords))
        _click(img.cords[0], img.cords[1])

    # Sample images aren't always going to be accurate because the OS changes the background
    # color based on the time of day, wallpaper, etc.
    # So you might have to change the sample image to get it to work
    images = [
        'sample/siri.png',
        'sample/apple.png',
        'sample/control center.png',
        'sample/green circle.png',
        'sample/finder.png'
    ]

    for i in images:
        _tester(i)
        exit(0)
