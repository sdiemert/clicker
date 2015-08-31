var express = require('express');
var router  = express.Router();

var members = [
    {memberId: "scienceventure", memberName: "Science Venture"},
    {memberId: "scienceventure", memberName: "Science Venture"}
];

/* GET home page. */
router.get('/', function (req, res, next) {
    res.render('index', {});
});

router.get("/home", function (req, res, next) {
    res.render("home", {members:members});
});

module.exports = router;
