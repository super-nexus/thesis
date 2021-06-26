package si.uni_lj.fri.pbd.thesisapp

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.EditText
import com.fasterxml.jackson.databind.ObjectMapper
import com.github.kittinunf.fuel.Fuel
import com.github.kittinunf.fuel.core.extensions.jsonBody
import com.github.kittinunf.fuel.httpPost
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.io.IOException
import java.net.HttpURLConnection
import java.net.URL

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
            }
            else{
            }

        }catch (error: IOException){
            Log.i("andrija", error.toString())
        }
    }


}