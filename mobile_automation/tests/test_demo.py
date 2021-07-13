from core.base_case import BaseCase
import logging

log = logging.getLogger('main_logger')

class TestDemo(BaseCase):

    def test_01(self):
        log.info("Hello first test")
        self.current_page.get_username_input().send_keys("Hello world")
        assert self.current_page.get_username_input().text == "Hello world", "Username should be equal to hello world"

    def test_02(self):
        log.info("Correct login")
        log.info("Checking if username and password input fields are visible")
        assert self.current_page.get_username_input().is_displayed(), "Username input is not displayed"
        assert self.current_page.get_password_input().is_displayed(), "Password field is not displayed"
        log.info("Entering username and password")
        self.current_page.get_username_input().send_keys("Andrija")
        self.current_page.get_password_input().send_keys("Diploma")
        log.info("Tapping on login button")
        self.current_page.get_login_button().click()
        self.load_page('second_page')
        assert self.current_page.get_page_title().is_displayed(), "Page title not displayed"