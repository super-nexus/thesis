from core.base_case import BaseCase
import logging

log = logging.getLogger('main_logger')


class SecondTest(BaseCase):

    def setup_method(self):
        if self.current_page.__class__.__name__ == "LoginPage":
            self.current_page.login()

    def test_01_private_mode_switch(self):
        log.info("Verifying private mode switch")
        log.info("Verifying that switch is usable")
        self.current_page.is_element_usable(self.current_page.get_private_mode_switch, assertion=True)
        original_switch_state = self.get_switch_state()
        log.info(f"Current switch state is {original_switch_state}")
        log.info("Tapping on switch")
        self.current_page.get_private_mode_switch().click()
        log.info("Verifying that switch state has changed")
        current_switch_state = self.get_switch_state()
        assert current_switch_state != original_switch_state, "Switch state has not changed"
        log.info("Switch state updated successfully")

    def get_switch_state(self):
        return self.current_page.get_private_mode_switch().get_attribute('checked') == "true"