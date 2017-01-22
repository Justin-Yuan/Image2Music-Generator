const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const multer = require('multer');
const exec = require('child_process').exec;

var storage =   multer.diskStorage({
  destination: function (req, file, callback) {
    callback(null, './uploads');
  },
  filename: function (req, file, callback) {
    callback(null, file.fieldname + '-' + Date.now() + '.jpeg');
  }
});
const port = process.env.PORT || 3000;
var upload = multer({ storage: storage }).single('userPhoto');
// var router = express.Router();

// app.use(express.static('public'));

// handle home request
app.get('/',function(req,res){
      res.sendFile(__dirname + "/index.html");
});

// handle file upload request 
app.post('/api/photo',function(req,res){
    upload(req,res,function(err) {
        if(err) {
            return res.end("Error uploading file.");
        }
        exec('python printline.py', (error, stdout, stderr) => {
            if(error){
                console.log(`exec error: ${error}`);
                return;
            }
            console.log(`stdout: ${stdout}`);
            console.log(`stderr: ${stderr}`);
        });
        res.end("File is uploaded");
    });
});

// set default root for the routes 
// app.use('/', router);
// start the server 
app.listen(port, function(){
    console.log("Working on port " + port);
});