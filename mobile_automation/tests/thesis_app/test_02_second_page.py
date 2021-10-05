from core.base_case import BaseCase
from appium.webdriver.common.touch_action import TouchAction
import logging


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

    def test_02_settings_switch(self):
        settings = ["Settings 1", "Settings 2", "Settings 3"]
        for setting_name in settings:
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
        log.info("Hiding the keyboard")
        self.current_page.hide_keyboard()
        log.info("Tapping on the post button")
        self.current_page.get_post_button().click()
        log.info("Verifying that the post has been added")
        self.current_page.is_element_usable(lambda: self.current_page.get_post_by_index(0), assertion=True)
        log.info("Verifying that the text of the post mathches the entered text")
        assert self.current_page.get_post_by_index(0).text == first_post_text, \
            "Post text does not match the entered text"
        log.info("Post successfully added")

    def test_06_verify_slider(self):
        log.info("Verifying slider/seek bar")
        slider = self.current_page.get_seekbar()
        slider_label = self.current_page.get_seekbar_label()
        slider_start = 0
        slider_y = slider.size["height"] / 2
        width_percentage = 0.49 if self.current_page.is_android() else 0.455
        slider_end = slider_start + slider.size["width"] * width_percentage
        action = TouchAction(self.current_page.driver)
        log.info("Sliding the seek bar to 50%")
        action.press(slider, slider_start, slider_y).wait(1000).move_to(slider, slider_end - 1, slider_y).wait(1000).release().perform()
        assert slider_label.text == "50%", "Slider should be set to 50%"

    def get_switch_state(self):
        if self.current_page.is_android():
            return self.current_page.get_private_mode_switch().get_attribute('checked') == "true"
        else:
            return self.current_page.get_private_mode_switch().get_attribute('value') == '1'

    def get_setting_state(self, settings_name):
        return self.current_page.is_checked(lambda: self.current_page.get_settings_by_name(settings_name))

    def get_option_states(self, option_names):
        return [self.get_option_state(name) for name in option_names]

    def get_option_state(self, option_name):
        return self.current_page.is_checked(lambda: self.current_page.get_option_by_name(option_name))

    def comment_box_empty(self):
        return self.current_page.get_comment_box().text == ''