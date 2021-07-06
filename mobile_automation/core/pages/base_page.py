import pytest
from core.util import load_config
from core.webdriver import WebDriver
import pytest
import os
from importlib import import_module


class BasePage:

    def __init__(self):
        config_path = os.path.join(os.getcwd(), '..', 'configs', f'{pytest.config_name}.yaml')
        self.mobile_config = load_config(config_path)
        self.driver = WebDriver(self.mobile_config)
        self.driver.load_driver()
        self.platform = 'android' if self.driver.is_android() else 'ios'


