package si.uni_lj.fri.pbd.thesisapp

import android.annotation.SuppressLint
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.*
import android.widget.SeekBar.OnSeekBarChangeListener


class SecondActivity : AppCompatActivity() {

    companion object{
        public const val TAG = "myTag"
    }

    lateinit var commentBox: EditText
    lateinit var seekBar: SeekBar
    lateinit var seekBarLabel: TextView
    lateinit var commentListView: ListView
    lateinit var postButton: Button
    lateinit var listAdapter: ArrayAdapter<String>
    var comments = arrayListOf<String>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_second)
        initViews()
        postButton.setOnClickListener(postButtonClickedListener)
        seekBar.setOnSeekBarChangeListener(seekBarChangedListener)
        listAdapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, comments)
        commentListView.adapter = listAdapter

    }

    private val seekBarChangedListener = object: OnSeekBarChangeListener {

        @SuppressLint("SetTextI18n")
        override fun onProgressChanged(seekBar: SeekBar, i: Int, b: Boolean) {
            // Display the current progress of SeekBar
            seekBarLabel.text = "$i%"
        }

        override fun onStartTrackingTouch(seekBar: SeekBar) {
            // Do something
            Toast.makeText(applicationContext,"start tracking",Toast.LENGTH_SHORT).show()
        }

        override fun onStopTrackingTouch(seekBar: SeekBar) {
            // Do something
            Toast.makeText(applicationContext,"stop tracking",Toast.LENGTH_SHORT).show()
        }
    }

    private val postButtonClickedListener = View.OnClickListener {
        Log.i(TAG, "post button clicked")
        val inputedText = commentBox.text.toString()
        if(inputedText.isNotBlank()){
            listAdapter.add(inputedText)
        }
    }

    private fun initViews(){
        commentBox = findViewById(R.id.comment_box)
        seekBar = findViewById(R.id.seek_bar)
        seekBarLabel = findViewById(R.id.seek_bar_label)
        commentListView = findViewById(R.id.list_view)
        postButton = findViewById(R.id.post_button)
    }

}