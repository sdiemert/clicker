var express = require('express');
var router  = express.Router();

var util = require('util');

var userManager = require("../lib/UserManager")();
var initManager = require("../lib/InitiativeManager")();

router.get('/', function (req, res) {

    userManager.getUsers(null, function (err, m) {

        if (err) {

            return res.status(500);

        } else {

            initManager.getInits(null, function(err, inits){

                console.log(util.inspect(inits, false, null));

                res.status(200);
                return res.render('admin', {users : m, inits : inits});

            });



        }
    });

});

module.exports = router;
