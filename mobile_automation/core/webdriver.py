from appium import webdriver
from appium.webdriver.webdriver import WebDriver as BaseDriver


class WebDriver(BaseDriver):

    def __init__(self, config):
        self.config = config
        self.driver_loaded = False

    def load_driver(self):
        if self.driver_loaded:
            return

        desired_capabilities = {
            "platformName": self.config['platformName'],
            "deviceName": self.config['deviceName'],
            "automationName": self.get_automation_name(),
            "app": self.config['appPath']
        }

        super().__init__('http://127.0.0.1:4723/wd/hub', desired_capabilities)
        self.implicitly_wait(60)

        self.driver_loaded = True

    def get_automation_name(self):
        if self.is_android():
            return "UIAutomator2"
        elif self.is_ios():
            return "XCUItest"
        return "Invalid platform name"

    def is_android(self):
        return self.config['platformName'].lower() == "android"

    def is_ios(self):
        return self.config['platformName'].lower() == "ios"

    def get_device_name(self):
        return self.config['deviceName']