var express     = require('express');
var router      = express.Router();
var util        = require('util');
var users       = require('../lib/models/User').User;
var userManager = require("../lib/UserManager")();
var initManager = require("../lib/InitiativeManager")();

function auth(req, res, next) {

    if (req.session.user) {
        return next();
    }


    users.find(
        {
            name: {$regex : '^'+req.body.username+'$', $options : 'g'},
            password: {$regex : '^'+req.body.password+'$', $options : 'g'},
            admin : true
        }).exec(

        function (err, result) {

            if (err) {
                res.status(500);
                return res.send('ERROR DURING AUTHENTICATION');

            }

            if (!result || result.length !== 1) {
                res.status(401);
                return res.redirect('/admin/login');
            }

            req.session.user = {
                name: result[0].name
            };

            return next();

        }
    );

}

router.get('/',
    auth,
    function (req, res) {

        userManager.getUsers(null, function (err, m) {

            if (err) {

                return res.status(500);

            } else {

                initManager.getInits(null, function (err, inits) {

                    res.status(200);
                    return res.render('admin', {users: m, inits: inits});

                });

            }

        });

    });

router.get("/logout",
    function(req, res){
        delete req.session.user;
        return res.redirect('/home');
    }
);

router.get('/login',
    function (req, res) {

        return res.render("adminlogin");

    });


router.post('/login',
    auth,
    function (req, res) {
        res.redirect('/admin');
    });

module.exports = router;
