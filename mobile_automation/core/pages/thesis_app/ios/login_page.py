from core.pages.thesis_app.generic.login_page import LoginPage as BaseLoginPage


class LoginPage(BaseLoginPage):

    def get_username_input(self, **kwargs):
        return self.driver.find_element_by_accessibility_id('username_input', **kwargs)

    def get_password_input(self, **kwargs):
        return self.driver.find_element_by_accessibility_id('password_input', **kwargs)