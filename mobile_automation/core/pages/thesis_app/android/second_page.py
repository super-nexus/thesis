from core.pages.thesis_app.generic.second_page import SecondPage as BasePage


class SecondPage(BasePage):

    def get_page_title(self, **kwargs):
        return self.driver.find_element_by_id('page_title')
