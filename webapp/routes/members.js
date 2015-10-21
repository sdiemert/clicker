var express = require('express');
var router  = express.Router();

var util = require('util');

var memberManager = require("../lib/MemberManager")();
var eventManager  = require("../lib/EventManager")();

/**
 * Returns a list of members and their associated meta-data.
 */
router.get('/', function (req, res) {

    memberManager.getMembers(null, function (err, m) {

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

    memberManager.getMembers(".*" + req.params.name.toLowerCase() + ".*", function (err, result) {

        if (err) {

            console.log(err);
            res.status(500);
            return res.send(err);

        } else if (result.length !== 1) {

            console.log("invalid of numbers found that match: " + req.params.name.toLowerCase());
            res.status(500);
            return res.send();


        } else {

            eventManager.getEvents(req.params.name, null, null, function (err, events) {

                if (err) {

                    console.log(err);
                    res.status(500);
                    res.send();

                } else {

                    var agg = eventManager.aggregate(events);

                    eventManager.refine(agg, function (err, refined) {

                        if (req.params.format && req.params.format === 'json') {

                            return res.json({member: result[0], events: events});

                        } else {

                            console.log(util.inspect(refined));

                            return res.render('member', {
                                member       : result[0],
                                refined      : refined,
                                timeAggregate: eventManager.aggregateByDate(events)
                            });

                        }

                    });

                }

            });


        }

    });

});

router.post("/:member/:initiative/:tag/:timestamp/:user?", function (req, res) {

    eventManager.addEvent(req.params.member, req.params.initiative, req.params.tag, req.params.timestamp, req.params.user,
        function (err) {

            if (err) {
                console.log(err);
                res.status(500);
                return res.send(err);
            } else {

                res.status(200);
                return res.send();

            }

        }
    );

});

module.exports = router;
