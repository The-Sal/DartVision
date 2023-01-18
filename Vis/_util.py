import random
from utils2 import system


class ScreenShotError(Exception):
    pass

class ScreenShot:
    def __init__(self):
        self._file_name = None

    def _make_screen_shot(self):
        # screenshot with command line
        self._file_name = random.randint(0, 999999999).__str__() + '-dart-vision' + '.png'
        system.command(
            ['screencapture', self._file_name],
            waitUntilFinished=True
        )
        if not system.paths.fileExists(self._file_name):
            raise ScreenShotError('ScreenShotError: Failed to make screenshot')


    def __enter__(self):
        self._make_screen_shot()
        return self._file_name

    def __exit__(self, exc_type, exc_val, exc_tb):
        system.paths.remove(self._file_name)



class VisionError(Exception):
    pass

class UnableToFindImage(VisionError):
    pass


class PythonBinaryError(VisionError):
    pass


if __name__ == '__main__':
    with ScreenShot() as ss:
        print('Screenshot saved to: ' + ss)
        input('Press enter to delete screenshot')




