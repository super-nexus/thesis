from core.pages.thesis_app.thesis_app import ThesisApp as BasePage


class LoginPage(BasePage):

    def wait_page_loaded(self):
        return self.get_username_input(wait=20)