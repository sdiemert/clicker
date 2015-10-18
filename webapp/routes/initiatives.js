var express = require('express');
var router  = express.Router();
var util = require('util');

var initManager  = require("../lib/InitiativeManager")();

router.get('/', function (req, res, next) {

    initManager.getInits(null, function(err, result){

        if(err){
            console.log(err);
            res.status(500);
            return res.send();
        }else{
            res.status(200);
            return res.json(result);
        }
    })

});

router.post('/add/initiative/:name', function(res,req){

    initManager.addInit(null, function(err, result){

        if(err){
            console.log("Error:"+err);
            res.status(500);
            return res.send("ERROR");
        }else{
            console.log(util.inspect(result));
            res.status(200);
            return res.json(result);
        }

    });

});

module.exports = router;
