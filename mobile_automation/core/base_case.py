from core.util import get_class_name
import pytest
import logging
from core.util import load_config
from core.webdriver import WebDriver
from importlib import import_module

log = logging.getLogger('main_logger')


class BaseCase:

    @classmethod
    def setup_class(cls):
        log.info("Starting test cases")
        log.info("Loading driver")
        cls.init_driver()
        log.info("Loading initial page")
        cls.data = {
            'base_page': cls.load_initial_page()
        }
        log.info("Initial page loaded")

    @classmethod
    def teardown_class(cls):
        log.info("Test cases done")

    @classmethod
    def init_driver(cls):
        driver = WebDriver(config=load_config(pytest.config_path))
        if driver.driver_loaded:
            driver.reload_driver()
        else:
            driver.load_driver()

    @classmethod
    def load_initial_page(cls):
        app_name = pytest.app_name
        page_module = import_module(f'core.pages.{app_name}.{app_name}')
        app_class = getattr(page_module, get_class_name(app_name))
        app_base_page = app_class()
        return app_base_page.load_first_page()

    def load_page(self, page_name):
        page_module = import_module(f'core.pages.{pytest.app_name}.{self.data["base_page"].platform}.{page_name}')
        page = getattr(page_module, get_class_name(page_name))
        page_obj = page()
        if page_obj.wait_page():
            self.data['base_page'] = page_obj
            return page_obj
        else:
            raise TimeoutError("Page has exceeded load time")

    @property
    def current_page(self):
        return self.data['base_page']
