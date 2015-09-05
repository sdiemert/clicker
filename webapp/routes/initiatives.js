var express = require('express');
var router  = express.Router();

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

module.exports = router;
