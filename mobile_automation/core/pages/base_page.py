import pytest
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep
from core.util import load_config
from core.webdriver import WebDriver
from core.util import get_class_name
import pytest
import os
import logging
from importlib import import_module

log = logging.getLogger('main_logger')


class BasePage:

    def __init__(self):
        config_path = os.path.join(os.getcwd(), '..', 'configs', f'{pytest.config_name}.yaml')
        self.mobile_config = load_config(config_path)
        self.driver = WebDriver(self.mobile_config)
        self.driver.load_driver()
        self.platform = 'android' if self.driver.is_android() else 'ios'

    def wait_page(self):
        return True

    def load_page(self, page_name):
        page_module = import_module(f'core.pages.{pytest.app_name}.{self.platform}.{page_name}')
        page = getattr(page_module, get_class_name(page_name))
        page_obj = page()
        if page_obj.wait_page():
            return page_obj
        else:
            raise TimeoutError("Page has exceeded load time")

    def are_elements_visible(self, elements, assertion=False):
        for element in elements:
            current_element_visible = self.is_element_visible(element, assertion)
            if not current_element_visible:
                return False
        return True

    def is_element_visible(self, element, assertion=False):
        element_visible = element().is_displayed()
        if assertion:
            assert element_visible, "Element is not visible"
        return element_visible

    def are_elements_usable(self, elements, assertion=False):
        for element in elements:
            if not self.is_element_usable(element):
                return False
        return True

    def is_element_usable(self, element, assertion=False):
        try:
            log.info(f"checking if {element.__name__} is usable")
            element()
            return True
        except NoSuchElementException:
            if assertion:
                assert False, f"Element {element.__name__} is unusable"
            return False

    def validate_elements_enabled(self, element_handlers, **kwargs):
        self.validate_elements_attributes(element_handlers=element_handlers,
                                          attribute='enabled', attr_value='true', **kwargs)

    def validate_elements_displayed(self, element_handlers, **kwargs):
        if self.driver.is_android():
            self.validate_elements_attributes(element_handlers=element_handlers,
                                              attribute='displayed', attr_value='true', **kwargs)
        else:
            self.validate_elements_attributes(element_handlers=element_handlers,
                                              attribute='visible', attr_value='true', **kwargs)


    def scroll_page(self, direction='down', **kwargs):
        """Scrolls whole page in direction (up/down/left/right)"""
        return self.driver.scroll_page(direction=direction, **kwargs)

    def validate_elements_attributes(self, element_handlers, attribute, attr_value, **kwargs):
        for handler in element_handlers:
            method_name = repr(handler).split('.')[1].split()[0]
            page_class = repr(handler).split('.pages.')[-1].split()[0].split('.')[-1]
            log.info(f'Check if {attribute} is {attr_value} in "{page_class}.{method_name}()"')
            element = handler(**kwargs)
            element.highlight_element()
            with element.suppress_w3c:
                log.info(f'"{handler}" is not {attr_value} on the current page')
                assert element.get_attribute(
                    attribute) == attr_value, f'"{handler}" is not {attr_value} on the current page'

    def scroll_to_element(self, element_getter, scroll_limit=4, scroll_direction='down', el_position=None, **kwargs):
        """Looks for an element by scrolling the whole screen.
        Remember to scroll both ways if you start from the middle."""

        def get_el_reference_point(pos, el):
            rect = el.rect
            if pos == 'top':
                return rect['y']
            elif pos == 'center':
                return int(rect['y'] + (rect['height'] / 2))
            elif pos == 'bottom':
                return rect['y'] + rect['height']

        found_element = None
        window = self.driver.get_window_size()
        window_h = window['height']
        pos_dict = {'top': 0.15, 'center': 0.5, 'bottom': 0.85}
        for _ in range(scroll_limit):
            try:
                found_element = element_getter(**kwargs)
                if not found_element.is_usable():
                    raise TimeoutException
                if el_position:  # if el_position is given then set the element on the given position
                    ref_point = get_el_reference_point(el_position, found_element) / window_h
                    if pos_dict[el_position] - 0.1 < ref_point < pos_dict[el_position] + 0.1:
                        break

                    elif ref_point < pos_dict[el_position]:
                        scroll_direction = 'up'
                        if not self.driver.is_android():
                            pos_dict = {'top': 0.4, 'center': 0.5, 'bottom': 0.6}  # iOS needs smaller values
                        thr_kwargs = {'thr1': ref_point, 'thr2': pos_dict[el_position]}

                    elif ref_point > pos_dict[el_position]:
                        scroll_direction = 'down'
                        if not self.driver.is_android():
                            pos_dict = {'top': 0.4, 'center': 0.5, 'bottom': 0.6}  # iOS needs smaller values
                        thr_kwargs = {'thr2': ref_point, 'thr1': pos_dict[el_position]}

                    self.scroll_page(direction=scroll_direction, duration=1)

                break
            except TimeoutException:
                log.info('Scrolling page')
                self.scroll_page(direction=scroll_direction)
                sleep(1)
        return found_element
