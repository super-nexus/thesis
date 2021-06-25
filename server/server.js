var express = require('express');
const bodyParser = require('body-parser');


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

    console.log(req.body)

    if(givenUsername && givenPassword){
        if(givenUsername == username && givenPassword == password){
            res.status(200).send("OK");
        }
        else{
            res.status(200).send("INCORRECT CREDENTIALS");
        }
    }
    else{
        res.status(401).send("BAD REQUEST");
    }

})

var server = app.listen(8081, function(){
    var host = server.address().address
    var port = server.address().port
    
    console.log("Example app listening at http://%s:%s", host, port)
})