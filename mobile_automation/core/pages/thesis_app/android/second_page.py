from core.pages.thesis_app.generic.second_page import SecondPage as BasePage


class SecondPage(BasePage):

    def get_page_title(self, **kwargs):  # Username
        return self.driver.find_element_by_id('username_label', **kwargs)

    def get_seekbar(self, **kwargs):
        return self.driver.find_element_by_id('seek_bar', **kwargs)

    def get_seekbar_label(self, **kwargs):
        return self.driver.find_element_by_id('seek_bar_label', **kwargs)

    def get_private_mode_switch(self, **kwargs):
        return self.driver.find_element_by_id('private_mode_switch', **kwargs)

    def get_settings_by_name(self, name, **kwargs):
        return self.driver.find_element_by_xpath(
            f'//android.widget.CheckBox[@text="{name}"]', **kwargs)

    def get_option_by_name(self, name, **kwargs):
        return self.driver.find_element_by_xpath(
            f'//android.widget.RadioButton[@text="{name}"]', **kwargs)

    def get_comment_box(self, **kwargs):
        return self.driver.find_element_by_id('comment_box', **kwargs)

    def get_post_button(self, **kwargs):
        return self.driver.find_element_by_id('post_button', **kwargs)

    def get_post_by_index(self, index=0, **kwargs):
        return self.driver.find_element_by_xpath(
            f'//android.widget.ListView/android.widget.TextView[@index={index}]', **kwargs)
