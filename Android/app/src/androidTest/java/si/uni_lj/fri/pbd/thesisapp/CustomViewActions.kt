package si.uni_lj.fri.pbd.thesisapp

import android.view.View
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.PerformException
import androidx.test.espresso.UiController
import androidx.test.espresso.ViewAction
import androidx.test.espresso.matcher.ViewMatchers.*
import androidx.test.espresso.util.HumanReadables
import androidx.test.espresso.util.TreeIterables
import java.util.concurrent.TimeoutException
import org.hamcrest.Matcher

object CustomViewActions {

    // CustomViewActions.kt:
    /**
     * This ViewAction tells espresso to wait till a certain view is found in the view hierarchy.
     * @param viewId The id of the view to wait for.
     * @param timeout The maximum time which espresso will wait for the view to show up (in milliseconds)
     */
    fun waitForView(viewText: String, timeout: Long): ViewAction {

        return object : ViewAction {
            override fun getConstraints(): Matcher<View> {
                return isRoot()
            }

            override fun getDescription(): String {
                return "wait for a specific view with text $viewText; during $timeout millis."
            }

            override fun perform(uiController: UiController, rootView: View) {
                uiController.loopMainThreadUntilIdle()
                val startTime = System.currentTimeMillis()
                val endTime = startTime + timeout
                val viewMatcher = withText(viewText)

                do {
                    // Iterate through all views on the screen and see if the view we are looking for is there already
                    for (child in TreeIterables.breadthFirstViewTraversal(rootView)) {
                        // found view with required ID
                        if (viewMatcher.matches(child)) {
                            return
                        }
                    }
                    // Loops the main thread for a specified period of time.
                    // Control may not return immediately, instead it'll return after the provided delay has passed and the queue is in an idle state again.
                    uiController.loopMainThreadForAtLeast(100)
                } while (System.currentTimeMillis() < endTime) // in case of a timeout we throw an exception -> test fails
                throw PerformException.Builder()
                    .withCause(TimeoutException())
                    .withActionDescription(this.description)
                    .withViewDescription(HumanReadables.describe(rootView))
                    .build()
            }
        }
    }

}