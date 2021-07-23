import pytest

from core.base_case import BaseCase
import logging
import numpy as np

log = logging.getLogger('main_logger')



class Test02SecondPage(BaseCase):

    def setup_method(self, method):
        if self.current_page.__class__.__name__ == "LoginPage":
            self.current_page.login()
            self.load_page('second_page')

    def teardown_method(self, method):
        if self.current_page.is_element_usable(self.current_page.get_comment_box) and not self.comment_box_empty():
            log.info("Clearing comment box")
            self.current_page.get_comment_box().clear()

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

    @pytest.mark.parametrize('setting_name', ["Settings 1", "Settings 2", "Settings 3"])
    def test_02_settings_switch(self, setting_name):
        log.info("Verifying settings checkboxes")
        log.info("Getting checkboxes state")
        original_settings_state = self.get_setting_state(setting_name)
        log.info(f"Tapping on the setting {setting_name}")
        self.current_page.get_settings_by_name(setting_name).click()
        log.info("Verifying state has changed")
        current_settings_state = self.get_setting_state(setting_name)
        assert original_settings_state != current_settings_state, \
            f"Setting state for setting {setting_name} hasn't been updated"
        log.info("All settings updated successfully")

    def test_03_option_buttons(self):
        log.info("Verifying option buttons work")
        option_names = ["Option 1", "Option 2", "Option 3"]
        original_option_state = self.get_option_states(option_names)
        log.info(f"Tapping on {option_names[0]}")
        self.current_page.get_option_by_name(option_names[0]).click()
        log.info("Verifying that option state has changed")
        new_option_state = self.get_option_state(option_names[0])
        assert new_option_state != original_option_state[0], "Option state did not change"
        log.info(f"Tapping on {option_names[1]}")
        self.current_page.get_option_by_name(option_names[1]).click()
        log.info("Verifying that only one option is selected")
        current_option_states = self.get_option_states(option_names)
        for i in range(len(current_option_states)):
            if i != 1:
                assert not current_option_states[i], "Radio button shouldn't be enabled"
        log.info("Success: only one radio button is selected")

    def test_04_write_comment(self):
        log.info("Check if you can write a comment")
        self.current_page.is_element_usable(self.current_page.get_comment_box, assertion=True)
        comment = "This is an example of a comment"
        log.info(f'Entering "{comment}" into comment box')
        self.current_page.get_comment_box().send_keys(comment)
        log.info("Verifying that entered text is visible")
        assert self.current_page.get_comment_box().text == comment, f'Entered text should be equal to "{comment}"'

    def test_05_verify_posts(self):
        log.info("Verifying posts")
        first_post_text = "First post text"
        log.info(f'Entering "{first_post_text}" into comment box')
        self.current_page.get_comment_box().send_keys(first_post_text)
        log.info("Tapping on the post button")
        self.current_page.get_post_button().click()
        log.info("Verifying that the post has been added")
        self.current_page.is_element_usable(lambda: self.current_page.get_post_by_index(0), assertion=True)
        log.info("Verifying that the text of the post mathches the entered text")
        assert self.current_page.get_post_by_index(0).text == first_post_text, \
            "Post text does not match the entered text"
        log.info("Post successfully added")

    def get_switch_state(self):
        return self.current_page.get_private_mode_switch().get_attribute('checked') == "true"

    def get_setting_state(self, settings_name):
        return self.current_page.get_settings_by_name(settings_name)

    def get_option_states(self, option_names):
        return [self.get_option_state(name) for name in option_names]

    def get_option_state(self, option_name):
        return self.current_page.get_option_by_name(option_name).get_attribute('checked') == "true"

    def comment_box_empty(self):
        return self.current_page.get_comment_box().text == ''