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
import androidx.test.filters.SmallTest
import kotlinx.coroutines.delay
import org.hamcrest.CoreMatchers.*
import org.hamcrest.Matcher
import si.uni_lj.fri.pbd.thesisapp.CustomViewActions.waitForView
import org.hamcrest.core.StringContains.containsString


import org.junit.Test
import org.junit.runner.RunWith

import org.junit.Assert.*
import org.junit.Before
import org.junit.Rule
import si.uni_lj.fri.pbd.thesisapp.CustomViewActions.setProgress
import java.util.concurrent.TimeoutException

/**
 * Instrumented test, which will execute on an Android device.
 *
 * See [testing documentation](http://d.android.com/tools/testing).
 */
@RunWith(AndroidJUnit4::class)
@SmallTest
class SecondPageTest {

    @get:Rule
    var activityRule: ActivityScenarioRule<SecondActivity>
            = ActivityScenarioRule(SecondActivity::class.java)

    @Test
    fun privateModeSwitch(){
        onView(withId(R.id.private_mode_switch))
            .perform(click())
            .check(matches(isChecked()))
    }

    @Test
    fun check_checkboxes(){
        val checkBoxIds = listOf<Int>(R.id.checkBox, R.id.checkBox2, R.id.checkBox3)
        for(checkBoxId in checkBoxIds){
            onView(withId(checkBoxId))
                .check(matches(isNotChecked()))
                .perform(click())
                .check(matches(isChecked()))
        }
    }

    @Test
    fun radioButtons(){
        val radioButtonIds = listOf<Int>(R.id.radioButton, R.id.radioButton2, R.id.radioButton3)
        onView(withId(radioButtonIds[0]))
            .check(matches(isNotChecked()))
            .perform(click())
            .check(matches(isChecked()))

        onView(withId(radioButtonIds[1])).perform(click())

        for(i in 0..2 step 2){
            onView(withId(radioButtonIds[i])).check(matches(isNotChecked()))
        }
    }

    @Test
    fun commentBox(){
        val typedText = "This is an example of a comment"
        onView(withId(R.id.comment_box))
            .perform(typeText(typedText))
            .check(matches(withText(typedText)))
    }

    @Test
    fun verifyPosts(){
        val postText = "First post text"
        onView(withId(R.id.comment_box))
            .perform(typeText(postText), ViewActions.closeSoftKeyboard())
        onView(withId(R.id.post_button)).perform(click())
        onData(allOf(`is`(instanceOf(String::class.java)), `is`(postText)))
            .check(matches(withText(postText)))
    }

    @Test
    fun verifySeekBar(){
        onView(withId(R.id.seek_bar))
            .perform(setProgress(50))
        onView(withId(R.id.seek_bar_label))
            .check(matches(withText("50%")))
    }

}