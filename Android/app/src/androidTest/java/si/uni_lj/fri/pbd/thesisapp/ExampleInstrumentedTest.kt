package si.uni_lj.fri.pbd.thesisapp

import android.util.Log
import android.view.View
import androidx.test.espresso.matcher.ViewMatchers.*
import androidx.test.espresso.action.ViewActions.*
import androidx.test.espresso.Espresso.*
import androidx.test.espresso.PerformException
import androidx.test.espresso.UiController
import androidx.test.espresso.ViewAction
import androidx.test.espresso.action.ViewActions
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.util.HumanReadables
import androidx.test.espresso.util.TreeIterables
import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.hamcrest.CoreMatchers.allOf
import androidx.test.filters.SmallTest
import kotlinx.coroutines.delay
import org.hamcrest.Matcher
import si.uni_lj.fri.pbd.thesisapp.CustomViewActions.waitForView

import org.junit.Test
import org.junit.runner.RunWith

import org.junit.Assert.*
import org.junit.Before
import org.junit.Rule
import java.util.concurrent.TimeoutException

/**
 * Instrumented test, which will execute on an Android device.
 *
 * See [testing documentation](http://d.android.com/tools/testing).
 */
@RunWith(AndroidJUnit4::class)
@SmallTest
class ExampleInstrumentedTest {

    companion object{
        public const val TAG = "LoginTest"
    }

    @get:Rule
    var activityRule: ActivityScenarioRule<MainActivity>
            = ActivityScenarioRule(MainActivity::class.java)

    @Test
    fun useAppContext() {
        // Context of the app under test.
        val appContext = InstrumentationRegistry.getInstrumentation().targetContext
        assertEquals("si.uni_lj.fri.pbd.thesisapp", appContext.packageName)
    }

    @Test
    fun verify_input_fields(){
        val usernameInput = "Andrija"
        val passwordInput = "blalbla"

        log("Verifying input fields")
        log("Entering $usernameInput into username input")
        onView(withId(R.id.username_input))
            .perform(typeText(usernameInput), ViewActions.closeSoftKeyboard())
            .check(matches(withText(usernameInput)))
        log("Entering $passwordInput into password input")
        onView(withId(R.id.password_input))
            .perform(typeText(passwordInput))
            .check(matches(withText(passwordInput)))
    }

    @Test
    fun incorrect_login(){
        val usernameInput = "Andrija"
        val passwordInput = "djdaksjk"

        loginWith(username = usernameInput, password = passwordInput)

        onView(isRoot()).perform(waitForView("Incorrect credentials", 5000))
        onView(withText("TRY AGAIN")).check(matches(isDisplayed()))
    }

    @Test
    fun correctLogin(){
        loginWith(username = "Andrija", password = "Diploma")
    }

    private fun loginWith(username: String, password: String){
        onView(withId(R.id.username_input))
            .perform(typeText(username), ViewActions.closeSoftKeyboard())

        onView(withId(R.id.password_input))
            .perform(typeText(password))

        onView(withId(R.id.login_button)).perform(click())
    }

    private fun log(message: String){
        Log.d(TAG, message)
    }

}

