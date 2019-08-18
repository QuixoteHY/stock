var express = require('express');
var app = express();
var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/";
// --registry=https://registry.npm.taobao.org

app.get('/get11', function (req, res) {
    exports.result = MongoClient.connect(url, { useNewUrlParser: true }, function(err, db) {
        if (err) throw err;
jjjj        var where_str = {"ts_code": "000001_SZ", "indicator_code": "0015", "time": /20(1[876543210]|0[9])1231/i}
        var result = dbo.collection("fi").find(where_str).toArray(function(err, result) {
            if (err) throw err;
//            console.log(result);
            db.close();
            return result;
        });
        return result;
    });
    console.log(result);
   res.send(result);
})

app.get('/get', function (req, res) {
    var db = MongoClient.connect('mongodb://localhost:27017/stock');
    var where_str = {"ts_code": "000001_SZ", "indicator_code": "0015", "time": /20(1[876543210]|0[9])1231/i};
    result = db.fi.find(where_str);
    console.log(result);
    db.close();
    res.send(result);
})

var server = app.listen(8082, function () {

  var host = server.address().address
  var port = server.address().port

  console.log("web server: http://%s:%s", host, port)

})
