from core.pages.thesis_app.thesis_app import ThesisApp as BasePage


class SecondPage(BasePage):

    def wait_page(self):
        return self.get_page_title(wait=20)

    def hide_keyboard(self):
        self.get_page_title().click()