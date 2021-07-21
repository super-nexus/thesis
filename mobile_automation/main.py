from appium import webdriver


desired_capabilities_android = {
    "platformName": "Android",
    "deviceName": "Pixel_3a_API_30_x86",
    "automationName": "UIAutomator2",
    "app": '/Users/andrijakuzmanov/Documents/code/thesis/Android/app/debug/app-debug.apk'
}

desired_capabilities_ios = {
    "platformName": "iOS",
    "platformVersion": "14.5",
    "deviceName": "iPhone 8",
    "automationName": "XCUItest",
    "app": '/Users/andrijakuzmanov/Library/Developer/Xcode/DerivedData/thesis-ios-hclsszzhnwwqnxcvmbavtpajlbpg/Build/Products/Debug-iphonesimulator/thesis-ios.app'
}

wd = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_capabilities_ios)
wd.implicitly_wait(60)

wd.quit()
