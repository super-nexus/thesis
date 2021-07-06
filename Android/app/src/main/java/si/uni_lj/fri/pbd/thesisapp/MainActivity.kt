package si.uni_lj.fri.pbd.thesisapp

import android.content.DialogInterface
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.EditText
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import com.github.kittinunf.fuel.Fuel
import com.github.kittinunf.fuel.core.extensions.jsonBody
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.IOException


class MainActivity : AppCompatActivity() {

    lateinit var loginButton: Button
    lateinit var usernameInput: EditText
    lateinit var passwordInput: EditText
    private val httpScope = CoroutineScope(Dispatchers.IO)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        initViews()
        loginButton.setOnClickListener(loginListener)

    }

    private var loginListener = View.OnClickListener(){
        val currentUsername = usernameInput.text.toString()
        val currentPassword = passwordInput.text.toString()

        httpScope.launch {
            login(currentUsername, currentPassword)
        }

    }

    private fun initViews(){
        loginButton = findViewById(R.id.login_button)
        usernameInput = findViewById(R.id.username_input)
        passwordInput = findViewById(R.id.password_input)
    }

    private suspend fun login(username: String, password: String){
        try {
            val urlAddress = "https://andrija-thesis.herokuapp.com/login"
            val data = "{ \"username\": \"$username\", \"password\": \"$password\" }"

            val (_, _, result) = Fuel.post(urlAddress).jsonBody(data).responseString()
            val (payload, error) = result

            if(payload.equals("OK")){
                withContext(Dispatchers.Main){
                    val intent = Intent(this@MainActivity, SecondActivity::class.java)
                    startActivity(intent)
                }
            }
            else if(payload.equals("INCORRECT CREDENTIALS")){
                withContext(Dispatchers.Main){
                    showDialog("Incorrect credentials",
                        "You entered incorrect username or password. Do you want to try again?")
                }
            }
            else{
                withContext(Dispatchers.Main){
                    showDialog("Error has occured", "Server unable to process the sent data")
                }
            }

        }catch (error: IOException){
            Log.i("andrija", error.toString())
        }
    }

    private fun showDialog(title: String, description: String){
        AlertDialog.Builder(this)
            .setTitle(title)
            .setMessage(description) // Specifying a listener allows you to take an action before dismissing the dialog.
            // The dialog is automatically dismissed when a dialog button is clicked.
            .setPositiveButton("Try again",
                DialogInterface.OnClickListener { dialog, which ->
                    // Continue with delete operation
                }) // A null listener allows the button to dismiss the dialog and take no further action.
            .setIcon(android.R.drawable.ic_dialog_alert)
            .show()
    }

}