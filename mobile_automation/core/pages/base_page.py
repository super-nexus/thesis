from selenium.common.exceptions import TimeoutException, NoSuchElementException
from core.webdriver import WebDriver
from core.util import get_class_name
from importlib import import_module
import pytest
import logging

log = logging.getLogger('main_logger')


class BasePage:

    def __init__(self):
        self.driver = WebDriver()
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

    def clear_input(self, input):
        if input().text != "":
            input().clear()

    def is_android(self):
        return self.driver.is_android()

    def is_ios(self):
        return self.driver.is_ios()

    def is_checked(self, element):
        if self.is_android():
            return element().get_attribute('checked') == "true"
        else:
            return element().is_selected()

    def scroll_page(self, direction='down', **kwargs):
        """Scrolls whole page in direction (up/down/left/right)"""
        return self.driver.scroll_page(direction=direction, **kwargs)
