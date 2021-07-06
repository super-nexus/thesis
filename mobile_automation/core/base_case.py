from core.util import get_class_name
import pytest
import logging
from importlib import import_module

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BaseCase:

    @classmethod
    def setup_class(cls):
        logger.info("Starting test cases")
        print("Loading initial page")
        cls.current_page = cls.load_initial_page()

    @classmethod
    def teardown_class(cls):
        logger.info("Test cases done")

    @classmethod
    def load_initial_page(cls):
        app_name = pytest.app_name
        page_module = import_module(f'core.pages.{app_name}.{app_name}')
        app_class = getattr(page_module, get_class_name(app_name))
        app_base_page = app_class()
        return app_base_page.load_first_page()