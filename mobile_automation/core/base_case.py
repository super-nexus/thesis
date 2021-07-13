from core.util import get_class_name
import pytest
import logging
from importlib import import_module

log = logging.getLogger('main_logger')


class BaseCase:

    @classmethod
    def setup_class(cls):
        log.info("Starting test cases")
        log.info("Loading initial page")
        cls.base_page = cls.load_initial_page()

    @classmethod
    def teardown_class(cls):
        log.info("Test cases done")

    @classmethod
    def load_initial_page(cls):
        app_name = pytest.app_name
        page_module = import_module(f'core.pages.{app_name}.{app_name}')
        app_class = getattr(page_module, get_class_name(app_name))
        app_base_page = app_class()
        return app_base_page.load_first_page()

    def load_page(self, page_name):
        page_module = import_module(f'core.pages.{pytest.app_name}.{self.base_page.platform}.{page_name}')
        page = getattr(page_module, get_class_name(page_name))
        page_obj = page()
        if page_obj.wait_page():
            self.base_page = page_obj
            return page_obj
        else:
            raise TimeoutError("Page has exceeded load time")

    @property
    def current_page(self):
        return self.base_page
