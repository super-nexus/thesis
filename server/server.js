var express = require('express');
const bodyParser = require('body-parser');

const port = process.env.PORT || 8081;

var app = express();
app.use(bodyParser.json());


let username = "Andrija"
let password = "Diploma"

app.get("/test", (req, res) => {
    res.status(200).send("Hello world")
})

app.post("/login", (req, res) => {
    
    let givenUsername = req.body["username"];
    let givenPassword = req.body["password"];

    console.log("Request received: ", req.body)

    if(givenUsername && givenPassword){
        if(givenUsername == username && givenPassword == password){
            res.status(200).send("OK");
        }
        else{
            res.status(200).send("INCORRECT CREDENTIALS");
        }
    }
    else{
        res.status(200).send("BAD REQUEST");
    }

})

var server = app.listen(port, function(){
    var host = server.address().address
    var port = server.address().port
    
    console.log("Example app listening at http://%s:%s", host, port)
})