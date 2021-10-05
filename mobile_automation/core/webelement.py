import time
import logging
from selenium.webdriver.remote import webelement
from selenium.webdriver.common.action_chains import ActionChains
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException, \
    WebDriverException, ElementNotInteractableException, TimeoutException, InvalidElementStateException


log = logging.getLogger('main_logger')


class MyWebElement(webelement.WebElement):

    def set_find_method(self, driver):
        # keeps the find method in the memory, to reinitialize the element
        self.driver = driver

    @property
    def action_chains(self):
        return ActionChains(self.opensync_web.driver)

    @property
    def touch_action(self):
        return TouchAction(self.opensync_web.driver)

    @property
    def location(self):
        return self._get_property('location')

    @property
    def size(self):
        return self._get_property('size')

    @property
    def rect(self):
        return self._get_property('rect')

    def _get_property(self, name):
        for _ in range(10):
            try:
                prop = getattr(webelement.WebElement, name).fget(self)
                if all(value == 0 for value in prop.values()):  # on iOS some elements return all 0's
                    self.reinit_element()
                    time.sleep(1)
                    continue
                return prop
            except Exception as e:
                if 'Invalid number value (infinite) in JSON write' in str(e):
                    log.info('Invalid number value (infinite) in JSON has occurred')
                    time.sleep(0.5)
                    continue
                elif type(e) == StaleElementReferenceException:
                    log.warn('StaleElementReferenceException has occurred')
                    self.reinit_element()
                    continue
                raise
        else:
            raise

    @property
    def checked(self):
        """Indicates if switch element is checked"""
        return True if self.get_attribute('checked') == 'true' else False

    def hover(self, screenshot=True):
        self.action_chains.move_to_element(self).perform()
        self.highlight_element(screenshot=screenshot)

    def action_click(self, screenshot=True):
        self.highlight_element(screenshot=screenshot)
        self.action_chains.move_to_element(self).click(self).perform()

    def delete_last_screenshot(self):
        self.log_catcher.delete_last_screenshot('test_screenshots.png', append=True)

    def _send_keys(self, *value):
        return super().send_keys(*value)

    def send_keys(self, *value, scroll='auto', screenshot=True, hide_value=False, key=None, skip_hide_keyboard=False):
        """Clicks the element."""
        # if not self.opensync_web.current_page.is_android():
        super().click()
        # workaround for InvalidElementStateException
        try:
            self._send_keys(*value)
        except InvalidElementStateException as e:
            log.warn(f'"{e}" has occured. Reinitializing element')
            self.reinit_element()
            self._send_keys(*value)

        self.highlight_element(screenshot=screenshot)
        if not skip_hide_keyboard:
            self.opensync_web.driver.hide_keyboard()

    def click(self, screenshot=True, timeout=9, retries=1):
        """Parameters:
            timeout - maximum timeout for click response in s
            retries - number of retries after StaleElementException"""
        self.highlight_element(screenshot=screenshot)
        for _ in range(3):
            timer = time.time()
            self.click_with_retries(retries)
            if time.time() - timer > timeout:  # 9.46 is the fastest response for failed click
                log.warn(f'Click response too long: {time.time() - timer:.2f}s]')
                self.reinit_element()  # repeating clicks is not enough
                time.sleep(1)
                self.highlight_element(screenshot=screenshot)
                continue
            break
        else:
            raise Exception('Click method failed 3 times in a row')

    def click_with_retries(self, retries=1):
        if retries:
            for _ in range(retries):
                try:
                    super().click()
                    break
                except StaleElementReferenceException:
                    log.warn(f'Stale Element Exception has occured. Trying click() {retries - _ - 1} more times.')
                    self.reinit_element()
                    continue

    def tap(self, count=1, screenshot=True, tap_position='center'):
        """Taps in the middle of the element"""
        element_rect = self.rect
        target = None
        # touch_action.tap uses top left corner as a default value, so we can calculate the center of the element
        # on the page and pass to it tap function without the first argument which is the element itself
        if tap_position == 'center':
            target = {'x': element_rect['x'] + int(element_rect['width'] / 2),
                      'y': element_rect['y'] + int(element_rect['height'] / 2),
                      'width': 10, 'height': 10}  # values for the highlight element
        if tap_position == 'left':
            target = {'x': element_rect['x'],
                      'y': element_rect['y'],
                      'width': 10, 'height': 10}  # values for the highlight element
        if tap_position == 'right':
            target = {'x': (element_rect['x'] + int(element_rect['width'])) * 0.95,
                      'y': (element_rect['y'] + int(element_rect['height'])) * 0.98,
                      'width': 10, 'height': 10}  # values for the highlight element
        self.highlight_element(target, screenshot=screenshot, draw_circle=True)
        self.touch_action.tap(None, target['x'], target['y'], count=count).perform()

    def tap_with_offset(self, x_offset=0, y_offset=0, count=1, screenshot=True):
        """Taps on screen with an offset to the given element.
        Relative to the element's center point"""
        element_rect = self.rect
        target = {'width': 10, 'height': 10,
                  'x': element_rect['x'] + int(element_rect['width'] / 2) + x_offset,
                  'y': element_rect['y'] + int(element_rect['height'] / 2) + y_offset}
        if x_offset == y_offset == 0:
            log.warn('Tap offsets are set to 0. Tapping in the middle of the element.')
        self.highlight_element(rect=target, screenshot=screenshot, draw_circle=True)
        self.touch_action.tap(None, target['x'], target['y'], count).perform()

    def clear(self, skip_hide_keyboard=False):
        """Clears the field"""
        if self.opensync_web.current_page.is_android():
            super().clear()
        else:
            """clear() method is not working on IOS. To clear the field function taps twice, then clicks 'select
            all' and sends a backspace """
            if not skip_hide_keyboard:
                self.opensync_web.driver.hide_keyboard()  # hide keyboard to ensure that context menu will appear
            # in total tap 3 times: 1 - for the focus, 2 - to set the cursor, 3 - to open the context menu
            self.click()
            time.sleep(0.5)
            self.tap(screenshot=False)
            time.sleep(0.5)
            self.tap(screenshot=False)
            try:
                select_all = self.opensync_web.driver.find_element_by_ios_class_chain(
                    f'**/XCUIElementTypeMenuItem[`name=="{self.opensync_web.current_page.translate("select_all")}"`]',
                    wait=3)
                select_all.click()
                time.sleep(0.5)  # wait for the tex to highlight
                # send one backspace
                self._send_keys('\b')
                if not skip_hide_keyboard:
                    self.opensync_web.driver.hide_keyboard()  # hide keyboard after everything
            except TimeoutException:
                log.warn('"Select All" button could not be located. Field might be empty already')
                return False
            return True

    def calc_element_onscreen_percentage(self, screen_width, screen_height, x, y, w, h):
        intersecting_area = max(0, min(screen_width, x + w) - max(0, x)) * max(0, min(screen_height, y + h) - max(0, y))
        # percentage calculated relative to element
        if (w * h) == 0:
            return 0
        percent_overlap = intersecting_area / (w * h)
        return percent_overlap

    def is_usable(self):
        """Check if element is usable (element rectangle is at least partially contained in screen rectangle)"""
        try:
            self.highlight_element()
        except TimeoutException:
            return False
        window = self.opensync_web.driver.get_window_size()
        window_w = window['width']
        window_h = window['height']
        rect = self.rect
        w = rect['width']
        h = rect['height']
        x = rect['x']
        y = rect['y']
        onscreen_fraction = self.calc_element_onscreen_percentage(window_w, window_h, x, y, w, h)
        if onscreen_fraction <= 0:  # on android only visible rect is returned
            log.info(f'onscreen_fraction is < 0. Element rect: x={x}, y={y}, w={w}, h={h}')
            return False
        return True

    def scroll_element(self, direction='right'):
        """Scrolls specified element in direction (up/down/left/right)"""
        if self.opensync_web.current_page.is_android():
            rect = self.rect
            x = rect['x']
            y = rect['y']
            w = rect['width']
            h = rect['height']
            if direction == 'left':
                self.opensync_web.driver.swipe(w * 0.33 + x, h * 0.5 + y, w * 0.66 + x, h * 0.5 + y)
            elif direction == 'right':
                self.opensync_web.driver.swipe(w * 0.66 + x, h * 0.5 + y, w * 0.33 + x, h * 0.5 + y)
            elif direction == 'up':
                self.opensync_web.driver.swipe(w * 0.5 + x, h * 0.33 + y, w * 0.5 + x, h * 0.66 + y)
            else:  # down
                self.opensync_web.driver.swipe(w * 0.5 + x, h * 0.66 + y, w * 0.5 + x, h * 0.33 + y)
        else:
            self.opensync_web.driver.execute_script('mobile: scroll', {'direction': direction, 'element': self.id})

    def scroll_to_element(self, element_getter, scroll_limit=4,
                          scroll_direction='down', **kwargs):
        """Looks for an element by scrolling this element.
        Remember to scroll both ways if you start from the middle."""
        found_element = None
        for _ in range(scroll_limit):
            try:
                found_element = element_getter(**kwargs)
                if not found_element.is_usable():
                    raise TimeoutException
                break
            except TimeoutException:
                self.scroll_element(direction=scroll_direction)
        return found_element

    def drag(self, to_x, to_y, duration=1, screenshot=True):
        element_rect = self.rect
        self.highlight_element(screenshot=screenshot)
        if self.opensync_web.current_page.is_android():
            x = to_x - (element_rect['x'] - int(element_rect['width'] / 2))
            y = to_y - (element_rect['y'] - int(element_rect['height'] / 2))
            self.touch_action.press(self).wait(duration * 1000).move_to(None, x, y).release().perform()
        else:
            self.opensync_web.driver.execute_script('mobile: dragFromToForDuration',
                                                    {'duration': duration,
                                                     'fromX': element_rect['x'] + int(element_rect['width'] / 2),
                                                     'fromY': element_rect['y'] + int(element_rect['height'] / 2),
                                                     'toX': to_x,
                                                     'toY': to_y})
        self.highlight_element(screenshot=screenshot)
