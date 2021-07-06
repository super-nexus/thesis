import pytest
from core.pages.base_page import BasePage
from importlib import import_module


class ThesisApp(BasePage):

    def __init__(self):
        super().__init__()

    def load_first_page(self):
        page_module = import_module(f'core.pages.{pytest.app_name}.{self.platform}.login_page')
        initial_page = getattr(page_module, 'LoginPage')
        return initial_page()


