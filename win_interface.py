import win32api
import win32con

from ctypes import windll
from PIL import ImageGrab


def screenshot():
    user32 = windll.user32
    user32.SetProcessDPIAware()
    img = ImageGrab.grab()
    return img


class Mouse(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        return

    def getPos(self):
        self.x, self.y = win32api.GetCursorPos()
        return

    def setPos(self, x, y):
        self.x, self.y = x, y
        win32api.SetCursorPos((x, y))
        return

    def click(self, x, y, button='left'):
        # TODO: check for proper button inputs
        if button == 'left':
            down = win32con.MOUSEEVENTF_LEFTDOWN
            up = win32con.MOUSEEVENTF_LEFTUP
        elif button == 'right':
            down = win32con.MOUSEEVENTF_RIGHTDOWN
            up = win32con.MOUSEEVENTF_RIGHTUP
        else:
            down = win32con.MOUSEEVENTF_MIDDLEDOWN
            up = win32con.MOUSEEVENTF_MIDDLEUP

        self.setPos(x, y)
        win32api.mouse_event(down, 0, 0)
        win32api.mouse_event(up, 0, 0)
        return

    def doubleclick(self, x, y, button='left'):
        self.click(x, y, button=button)
        self.click(x, y, button=button)
        return

if __name__ == '__main__':
    import time

    mouse = Mouse()
    mouse.click(500, 400)
    time.sleep(0.5)
    mouse.click(500, 300, button='right')
    time.sleep(0.5)
    mouse.click(500, 200, button='middle')
    time.sleep(0.5)
    mouse.doubleclick(500, 200)

    img = screenshot()
    img.show()
