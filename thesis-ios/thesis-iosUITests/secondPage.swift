//
//  secondPage.swift
//  thesis-iosUITests
//
//  Created by Andrija Kuzmanov on 7/26/21.
//

import XCTest

class secondPage: XCTestCase {
    
    let app: XCUIApplication = XCUIApplication()
    
    override func setUpWithError() throws {
        // Put setup code here. This method is called before the invocation of each test method in the class.

        // In UI tests it is usually best to stop immediately when a failure occurs.
        continueAfterFailure = false

        // UI tests must launch the application that they test. Doing this in setup will make sure it happens for each test method.
        app.launch()
        login(app)

        // In UI tests it’s important to set the initial state - such as interface orientation - required for your tests before they run. The setUp method is a good place to do this.
    }

    override func tearDownWithError() throws {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
    }
    
    func login(_ app: XCUIApplication){
        loginWith(app: app, username: "Andrija", password: "Diploma")
    }
    
    func loginWith(app: XCUIApplication, username: String, password: String){
        let usernameInputField = app.textFields["username_input"]
        let passwordInputField = app.textFields["password_input"]
        
        usernameInputField.tap()
        usernameInputField.typeText(username)
        passwordInputField.tap()
        passwordInputField.typeText(password)
        app.buttons["login_button"].tap()
    }

    func testPrivateModeSwitch() throws {
        let private_switch = app.switches["private_mode_switch"]
        let original_switch_state = private_switch.value as? String
                                
        private_switch.tap()
        let current_switch_value = private_switch.value as? String
        XCTAssert(original_switch_state != current_switch_value)
    }
    
    func testCommentBox() throws {
        let commentBox = app.textViews["comment_box"]
        let comment = "This is an example of a comment"
        commentBox.tap()
        selectAll(textView: commentBox)
        commentBox.typeText(comment)
        hideKeyboard()
        XCTAssert(commentBox.value as? String == comment)
    }
    
    func testPosts() throws {
        let commentBox = app.textViews["comment_box"]
        let postText = "First post text"
        commentBox.tap()
        selectAll(textView: commentBox)
        commentBox.typeText(postText)
        hideKeyboard()
        app.buttons["post_button"].tap()
        XCTAssert(app.staticTexts[postText].waitForExistence(timeout: 2))
    }
    
    func testRadioButtons() throws {
        let options: [String] = ["Option 1", "Option 2", "Option 3"]
        let first_option_state = app.buttons[options[0]].isSelected
        app.buttons[options[0]].tap()
        XCTAssert(first_option_state != app.buttons[options[0]].isSelected)
        //Tapping on second option and verifying that other are unselected
        app.buttons[options[1]].tap()
        for option in options {
            if option == options[1]{
                continue
            }
            XCTAssert(!app.buttons[option].isSelected)
        }
    }
    
    func testCheckbox() throws {
        let settings: [String] = ["Settings 1", "Settings 2", "Settings 3"]
        for setting in settings {
            let current_button = app.buttons[setting]
            let original_button_state = current_button.isSelected
            current_button.tap()
            XCTAssert(original_button_state != current_button.isSelected)
        }
    }
    
    func testSlider() throws {
        let slider = app.sliders["slider"]
        slider.adjust(toNormalizedSliderPosition: 0.5)
        let sliderText = app.staticTexts.element(matching: .any, identifier: "slider_label").label
        XCTAssert(sliderText == "50%")
    }
    
    func selectAll(textView: XCUIElement){
        textView.press(forDuration: 1.2)
        app.menuItems["Select All"].tap()
    }
    
    func hideKeyboard(){
        app.staticTexts["Username"].tap()
    }
    
}
