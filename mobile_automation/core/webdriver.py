from appium import webdriver
import time
import logging
from appium.webdriver.webdriver import WebDriver as BaseDriver
from selenium.common.exceptions import TimeoutException


log = logging.getLogger('main_logger')


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class WebDriver(BaseDriver):

    def __init__(self, config):
        self.config = config
        self.driver_loaded = False

    def load_driver(self):
        if self.driver_loaded:
            return

        desired_capabilities = {
            "platformName": self.config['platformName'],
            "deviceName": self.config['deviceName'],
            "automationName": self.get_automation_name(),
            "app": self.config['appPath']
        }

        super().__init__('http://127.0.0.1:4723/wd/hub', desired_capabilities)
        self.implicitly_wait(60)

        self.driver_loaded = True

    def scroll_page(self, direction='down', thr1=0.33, thr2=0.66, offset=0.5, duration=0.1):
        """Scrolls whole page in direction (up/down/left/right)
            thr1 = threshold1 - x axis - % of screen to start from
            thr2 = threshold2 - y axis - % of screen to stop at
            offset - 2nd axis position on the screen - default in the middle
            duration - the duration of a scroll
        """
        w = self.get_window_size()['width']
        h = self.get_window_size()['height']
        if self.is_android():
            if direction == 'left':
                self.swipe(w * thr1, h * offset, w * thr2, h * offset)
            elif direction == 'right':
                self.swipe(w * thr2, h * offset, w * thr1, h * offset)
            elif direction == 'up':
                self.swipe(w * offset, h * thr1, w * offset, h * thr2)
            else:  # down
                self.swipe(w * offset, h * thr2, w * offset, h * thr1)
        else:
            if direction == 'left':
                self.execute_script('mobile: dragFromToForDuration',
                                    {'duration': duration, 'fromX': w * thr1, 'fromY': h * offset, 'toX': w * thr2,
                                     'toY': h * offset})
            elif direction == 'right':
                self.execute_script('mobile: dragFromToForDuration',
                                    {'duration': duration, 'fromX': w * thr2, 'fromY': h * offset, 'toX': w * thr1,
                                     'toY': h * offset})
            elif direction == 'up':
                self.execute_script('mobile: dragFromToForDuration',
                                    {'duration': duration, 'fromX': w * offset, 'fromY': h * thr1, 'toX': w * offset,
                                     'toY': h * thr2})
            else:  # down
                self.execute_script('mobile: dragFromToForDuration',
                                    {'duration': duration, 'fromX': w * offset, 'fromY': h * thr2, 'toX': w * offset,
                                     'toY': h * thr1})

    def get_automation_name(self):
        if self.is_android():
            return "UIAutomator2"
        elif self.is_ios():
            return "XCUItest"
        return "Invalid platform name"

    def is_keyboard_shown(self):
        # android might not hide the keyboard after the test thus it can be checked before the app started
        if self.is_android():
            return super().is_keyboard_shown()
        else:
            try:
                self.find_element_by_ios_class_chain('**/XCUIElementTypeKeyboard', wait=2)
                return True
            except TimeoutException:
                return False

    def hide_keyboard(self):
        def tap_outside():
            window_size = self.get_window_size()
            x = window_size['width'] - 10
            y = window_size['height'] / 6
            self.touch_action.tap(None, x, y, 1).perform()

        # Be cary using hide_keyboard() for Android, due to sometimes during hide keyboard
        # current page is changing to next or previous
        if self.opensync_web.is_android():
            if self.is_keyboard_shown():
                return super().hide_keyboard()
            else:
                log.warn('Skip hide keyboard, keyboard not shown')
                return

        time.sleep(0.5)  # Sometimes keyboard is not yet shown
        tap_outside()
        timeout = time.time() + 2
        while time.time() < timeout:
            if not self.is_keyboard_shown():
                break
            time.sleep(0.5)
        else:
            # sometimes iOS blocks hiding keyboard, it can be hidden by pressing "Done" button
            self.find_element_by_ios_class_chain('**/*[`label == "Done"`]').click()
            time.sleep(0.5)

        if self.is_keyboard_shown():
            raise Exception('Can not hide keyboard')

    def find_element_by_id(self, id_, wait=5):
        self.implicitly_wait(wait)
        return super().find_element_by_id(id_)

    def find_element_by_xpath(self, xpath, wait=5):
        self.implicitly_wait(wait)
        return super().find_element_by_xpath(xpath)

    def is_android(self):
        return self.config['platformName'].lower() == "android"

    def is_ios(self):
        return self.config['platformName'].lower() == "ios"

    def get_device_name(self):
        return self.config['deviceName']