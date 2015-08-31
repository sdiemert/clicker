var express = require('express');
var router  = express.Router();

var members = [
    {memberId: "scienceventure", memberName: "Science Venture"},
    {memberId: "scienceventure", memberName: "Science Venture"}
];

router.get('/', function (req, res, next) {

    res.status(200);
    return res.json(members);


});

router.get('/:name', function (req, res, next) {
    res.render('member', {});
});

module.exports = router;
