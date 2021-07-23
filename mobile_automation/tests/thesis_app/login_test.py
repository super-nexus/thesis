from core.base_case import BaseCase
import logging

log = logging.getLogger('main_logger')


class TestDemo(BaseCase):

    def setup_method(self):
        if self.popup_visible():
            log.info("Tapping on try again button")
            self.current_page.get_try_again_button().click()

    def test_01(self):
        log.info("Hello first test")
        self.current_page.get_username_input().send_keys("Hello world")
        assert self.current_page.get_username_input().text == "Hello world", "Username should be equal to hello world"

    def test_02(self):
        log.info("Incorrect login test")
        self.check_if_inputs_usable()
        self.login_with(username="Andrija", password="djdaksjk")
        log.info("Checking if the popup is displayed")
        self.popup_visible(assertion=True)
        log.info("Verifying that tapping on try again returns you to login screen")
        log.info("Tapping on try again button")
        self.current_page.get_try_again_button().click()
        self.check_if_inputs_usable()

    def test_03(self):
        log.info("Correct login")
        self.check_if_inputs_usable()
        self.login_with(username="Andrija", password="Diploma")
        self.load_page('second_page')
        assert self.current_page.get_page_title().is_displayed(), "Page title not displayed"

    def login_with(self, username, password):
        log.info(f"Entering username: {username} and password: {password}")
        self.current_page.get_username_input().send_keys(username)
        self.current_page.get_password_input().send_keys(password)
        log.info("Tapping on login button")
        self.current_page.get_login_button().click()

    def popup_visible(self, assertion=False):
        return self.current_page.are_elements_usable([
            self.current_page.get_popup_title,
            self.current_page.get_popup_description,
            self.current_page.get_try_again_button
        ], assertion)

    def check_if_inputs_usable(self):
        log.info("Checking if username and password input fields are visible")
        self.current_page.are_elements_usable([
            self.current_page.get_username_input,
            self.current_page.get_password_input
        ], assertion=True)
