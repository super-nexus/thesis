from core.pages.thesis_app.generic.login_page import LoginPage as BaseLoginPage


class LoginPage(BaseLoginPage):

    def get_username_input(self, **kwargs):
        return self.driver.find_element_by_accessibility_id('username_input', **kwargs)

    def get_password_input(self, **kwargs):
        return self.driver.find_element_by_accessibility_id('password_input', **kwargs)

    def get_login_button(self, **kwargs):
        return self.driver.find_element_by_accessibility_id('login_button', **kwargs)

    def get_popup_title(self, **kwargs):
        return self.driver.find_element_by_accessibility_id('Incorrect credentials', **kwargs)

    def get_try_again_button(self, **kwargs):
        return self.driver.find_element_by_accessibility_id('Try again', **kwargs)
