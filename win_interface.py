import win32api
import win32con
import win32gui
import win32ui
import cv2
import numpy as np

from ctypes import windll


class Screen(object):
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    user32 = windll.user32
    user32.SetProcessDPIAware()

    @classmethod
    def shot(cls):
        # grab a handle to the main desktop window
        hdesktop = win32gui.GetDesktopWindow()

        # create a device context
        desktop_dc = win32gui.GetWindowDC(hdesktop)
        img_dc = win32ui.CreateDCFromHandle(desktop_dc)

        # create a memory based device context
        mem_dc = img_dc.CreateCompatibleDC()

        # create a bitmap object
        screenshot = win32ui.CreateBitmap()
        screenshot.CreateCompatibleBitmap(img_dc, cls.width, cls.height)
        mem_dc.SelectObject(screenshot)

        # copy the screen into our memory device context
        mem_dc.BitBlt((0, 0), (cls.width, cls.height), img_dc, (cls.left, cls.top), win32con.SRCCOPY)

        # save the bitmap to a file
        signed_ints_array = screenshot.GetBitmapBits(True)
        screen_img = np.fromstring(signed_ints_array, dtype='uint8')
        screen_img = screen_img.reshape((cls.height, cls.width, 4))
        screen_img = cv2.cvtColor(screen_img, cv2.COLOR_RGBA2RGB)

        # free our objects
        img_dc.DeleteDC()
        mem_dc.DeleteDC()
        win32gui.ReleaseDC(hdesktop, desktop_dc)
        win32gui.DeleteObject(screenshot.GetHandle())
        return screen_img


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

    def leftClick(self, x, y):
        self.click(x, y)
        return

    def middleClick(self, x, y):
        self.click(x, y, button='middle')
        return

    def rightClick(self, x, y):
        self.click(x, y, button='right')
        return

    def __str__(self):
        return "x:%5d\ny:%5d" % (self.x, self.y)


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

    img = Screen.shot()
    cv2.imwrite('test.png', img)
