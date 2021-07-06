from core.base_case import BaseCase


class TestDemo(BaseCase):

    def test_01(self):
        print("Hello first test")
        self.current_page.get_username_input().send_keys("Hello world")
