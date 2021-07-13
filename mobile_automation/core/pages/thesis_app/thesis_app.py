import pytest
import logging
from core.pages.base_page import BasePage
from importlib import import_module

log = logging.getLogger('main_logger')


class ThesisApp(BasePage):

    def __init__(self):
        super().__init__()

    def load_first_page(self):
        return self.load_page("login_page")

    def login(self):
        log.info("Entering 'Andrija' to username input")
        self.get_username_input().send_keys('Andrija')
        log.info("Entering 'Diploma' to password input")
        self.get_password_input().send_keys('Diploma')
        log.info("Tapping on login button")
        self.get_login_button().click()
        self.load_page('second_page')
