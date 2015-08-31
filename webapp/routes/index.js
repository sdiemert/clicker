var express = require('express');
var router  = express.Router();

var memberManager = require("../lib/MemberManager")();


/* GET home page. */
router.get('/', function (req, res, next) {
    res.render('index', {});
});

router.get("/home", function (req, res, next) {

    memberManager.getMembers(".*", function(err, result){

        if(err){

            return res.render('error', {});

        }else{

            return res.render("home", {members : result});

        }

    });

});

module.exports = router;
