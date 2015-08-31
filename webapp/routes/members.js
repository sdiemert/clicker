var express = require('express');
var router  = express.Router();

var memberManager = require("../lib/MemberManager")();

/**
 * Returns a list of members and their associated meta-data.
 */
router.get('/', function (req, res, next) {

    memberManager.getMembers(null, function(err, m){

        if(err){
            return res.status(500);
        }else{
            res.status(200);
            return res.json(m);

        }
    });

});


/**
 * Renders a page with member information or returns a JSON string of the information.
 */
router.get('/:name/:format?', function (req, res, next) {

    if(req.params.format && req.params.format === 'json'){

        memberManager.getMembers();

        return res.json(members);

    }else{

        return res.render('member', {});

    }
});

module.exports = router;
