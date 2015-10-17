var express = require('express');
var router  = express.Router();

var util = require('util');

var userManager = require("../lib/UserManager")();
var eventManager  = require("../lib/EventManager")();

/**
 * Returns a list of members and their associated meta-data.
 */
router.get('/', function (req, res) {

    userManager.getUsers(null, function (err, m) {

        if (err) {
            return res.status(500);
        } else {
            res.status(200);
            return res.json(m);

        }
    });

});


/**
 * Renders a page with member information or returns a JSON string if the format is set to 'json'.
 */
router.get('/:name/:format?', function (req, res) {

    userManager.getUsers(".*" + req.params.name.toLowerCase() + ".*", function (err, result) {

        if (err) {

            console.log(err);
            res.status(500);
            return res.send(err);

        } else if (result.length !== 1) {

            console.log("invalid of numbers found that match: " + req.params.name.toLowerCase());
            res.status(500);
            return res.send();


        } else {

            console.log(util.inspect(result, false, null));

            console.log(result[0].pageContent);

            res.status(200);
            return res.render('user', {content : result[0].pageContent});

        }

    });

});


module.exports = router;
