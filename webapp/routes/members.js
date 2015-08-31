var express = require('express');
var router  = express.Router();

var Member = require("../lib/models/Member").Member;

var members = [
    {memberId: "scienceventure", memberName: "Science Venture"},
    {memberId: "scienceventure", memberName: "Science Venture"}
];

/**
 * Returns a list of members and their associated meta-data.
 */
router.get('/', function (req, res, next) {

    res.status(200);
    return res.json(members);

});


/**
 * Renders a list
 */
router.get('/:name', function (req, res, next) {
    res.render('member', {});
});

module.exports = router;
