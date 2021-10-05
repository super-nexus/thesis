//
//  thesis_iosUITests.swift
//  thesis-iosUITests
//
//  Created by Andrija Kuzmanov on 6/27/21.
//

import XCTest

class thesis_iosUITests: XCTestCase {

    override func setUpWithError() throws {
        // Put setup code here. This method is called before the invocation of each test method in the class.

        // In UI tests it is usually best to stop immediately when a failure occurs.
        continueAfterFailure = false

        // In UI tests it’s important to set the initial state - such as interface orientation - required for your tests before they run. The setUp method is a good place to do this.
    }

    override func tearDownWithError() throws {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
    }

    func testUsernameInput() throws {
        
        let app = XCUIApplication()
        app.launch()
        
        let usernameInput = "Hello world"
        let usernameInputField = app.textFields["username_input"]

        usernameInputField.tap()
        usernameInputField.typeText(usernameInput)
        XCTAssert(usernameInputField.value as! String == usernameInput)
    }
    
    func testIncorrectLogin() throws {
        // UI tests must launch the application that they test.
        let app = XCUIApplication()
        app.launch()
        
        let usernameInput = "Andrija"
        let passwordInput = "bla bla"
        loginWith(app: app, username: usernameInput, password: passwordInput)

        
        XCTAssert(app.staticTexts["Incorrect credentials"].waitForExistence(timeout: 5))
        XCTAssert(app.buttons["Try again"].waitForExistence(timeout: 5))
        
        // Use recording to get started writing UI tests.
        // Use XCTAssert and related functions to verify your tests produce the correct results.
    }
    
    func testCorrectLogin() throws {
        let app = XCUIApplication()
        app.launch()
        
        let usernameInput = "Andrija"
        let passwordInput = "Diploma"
        loginWith(app: app, username: usernameInput, password: passwordInput)
        
        XCTAssert(app.staticTexts["Username"].waitForExistence(timeout: 5))
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
    
}
