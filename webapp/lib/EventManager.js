/**
 * Created by sdiemert on 15-08-30
 */

var Event      = require("./models/Event").Event;
var Initiative = require("./models/Initiative").Initiative;
var Tag        = require("./models/Tag").Tag;

var util = require('util');

function EventManager(proc) {

    proc = proc || {};

    var that = {};

    /**
     *
     * Gets events that match the regular expressions provided.
     *
     * @param memberPattern {String} a regular expression to use to filter member _id, defaults to .*
     * @param initPattern {String} a regular expression to use to filter initiative _id, defaults to .*
     * @param tagPattern {String} a regular expression to use to filter tag _id, defaults to .*
     * @param next {Function} - has signature function(err {String}, result {Array}).
     */
    var getEvents = function (memberPattern, initPattern, tagPattern, next) {

        if (!next || typeof next !== "function" || next.length !== 2) {
            throw new Error("EventManager.getEvents(String, Function) expects second argument to be a function with arity 2.");
        }

        memberPattern = memberPattern || ".*";
        initPattern   = initPattern || ".*";
        tagPattern    = tagPattern || ".*";


        Event.find({
            member    : {$regex: memberPattern, $options: "g"},
            initiative: {$regex: initPattern, $options: "g"},
            tag       : {$regex: tagPattern, $options: "g"}
        }).exec(function (err, result) {

            if (err) {
                console.log(err);
                return next(err, null);
            } else {

                return next(null, result);

            }

        });

    };

    /**
     * @param pattern {String}  regular expression to match on initiative names, defautls to .*
     * @param next {Function} - has signature function(err {String}, result {Array})
     */
    var getInitiatives = function (pattern, next) {

        if (!next || typeof next !== "function" || next.length !== 2) {
            throw new Error("EventManager.getEvents(String, Function) expects second argument to be a function with arity 2.");
        }

        pattern = pattern || ".*";

        Initiative.find({

           id: {$regex: pattern, $options: "g"}

        }).exec(function (err, result) {

            if (err) {
                console.log(err);
                return next(err, null);
            } else {
                return next(null, result);
            }

        });

    };

    /**
     * @param pattern {String}  regular expression to match on tag names, defautls to .*
     * @param next {Function} - has signature function(err {String}, result {Array})
     */
    var getTags = function (pattern, next) {

        if (!next || typeof next !== "function" || next.length !== 2) {
            throw new Error("EventManager.getEvents(String, Function) expects second argument to be a function with arity 2.");
        }

        pattern = pattern || ".*";

        Tag.find({

            id: {$regex: pattern, $options: "g"}

        }).exec(function (err, result) {

            if (err) {
                console.log(err);
                return next(err, null);
            } else {
                return next(null, result);
            }

        });

    };

    /**
     * @param member {String}
     * @param initiative {String}
     * @param tag {String}
     * @param timestamp {String}
     * @param user {String{
     * @param next {Function}
     */
    var addEvent = function (member, initiative, tag, timestamp, user, next) {

        if (!next || typeof next !== 'function' || next.length !== 1 || !member || typeof member !== 'string' || !tag || typeof tag !== 'string' || !timestamp) {
            throw new Error("EventManager.addEvent(String, String, String, String, String, Function) expects 5 parameters, the last is a function or arity 1.")
        }

        timestamp = Number(timestamp);

        var e = new Event({initiative: initiative, member: member, tag: tag, user: user, time: timestamp});

        e.save(function (err, x) {
            return next(err);
        })


    };

    var replaceNames = function (data, inits, tags) {

        for (var i = 0; i < inits.length; i++) {

            for (var t = 0; t < tags.length; t++) {

                if (data[inits[i]] && data[inits[i].id][tags[t].id]) {

                    data[inits[i].id][tags[t].name] = data[inits[i].id][tags[t].id];
                    delete data[inits[i].id][tags[t].id];

                }

            }

            if (data[inits[i].id]) {
                data[inits[i].name] = data[inits[i].id];
                delete data[inits[i].id];
            }


        }

        return data;

    };

    var refine = function (data, outerCallback) {

        that.getInitiatives(null, function (ierr, inits) {

            that.getTags(null, function (terr, tags) {

                if (ierr) {

                    return outerCallback(ierr, null);

                } else if (terr) {

                    return outerCallback(terr, null);

                } else {

                    return outerCallback(null, replaceNames(data, inits, tags));

                }


            });

        });

    };

    /**
     * Aggregates the data for the events, sorted by the following (in order):
     *  - initiative
     *  - tag
     *  - timestamp
     *
     * @param data {Array}
     *
     * @return {Object} the aggregated data, has structure like:
     *  { initiative_name : { tag_name : { timestamp : Number }, ... }, ... } where timestamp is number of ms since epoch.
     */
    var aggregate = function (events) {

        var obj = {};

        var e        = null;
        var tmp_date = null;

        for (var i = 0; i < events.length; i++) {

            e = events[i];

            if (!obj[e.initiative]) {

                obj[e.initiative] = {};

            }

            if (!obj[e.initiative][e.tag]) {

                obj[e.initiative][e.tag] = {};

            }

            tmp_date = new Date(e.time * 1000);

            //set the time portion of the date to be 00:00:00.000
            // this causes all events from same day to have the same timestamp.
            tmp_date.setHours(0, 0, 0, 0);


            if (!obj[e.initiative][e.tag][tmp_date.getTime()]) {

                obj[e.initiative][e.tag][tmp_date.getTime()] = 0;

            }

            obj[e.initiative][e.tag][tmp_date.getTime()]++;

        }

        return obj;

    };

    /**
     * Aggregates event data by timestamp, rounds to nearest day.
     *
     * @param events {Array}
     * @returns {Object} has structure like:
     *  { timestamp : Number, ... } where timestamp is number of milliseconds since epoch.
     */
    var aggregateByDate = function (events) {

        var obj = {};

        var e        = null;
        var tmp_date = null;

        for (var i = 0; i < events.length; i++) {

            e = events[i];

            tmp_date = new Date(e.time * 1000);

            tmp_date.setHours(0, 0, 0, 0);

            if (!obj[tmp_date.getTime]) {

                obj[tmp_date.getTime()] = 0;

            }

            obj[tmp_date.getTime()]++;

        }

        return obj;
    };

    /**
     * Aggregates event data by initaitive
     *
     * @param events {Array}
     * @returns {Object} has structure like:
     *  { initiative_name : Number, ... }
     */
    var aggregateByInitiative = function (events) {

        var obj = {};

        var e = null;

        for (var i = 0; i < events.length; i++) {

            e = events[i];

            if (!obj[e.initiative]) {

                obj[e.initiative] = 0;

            }

            obj[e.initiative]++;

        }

        return obj;

    };


    that.getEvents             = getEvents;
    that.addEvent              = addEvent;
    that.getInitiatives        = getInitiatives;
    that.getTags               = getTags;
    that.refine                = refine;
    that.aggregate             = aggregate;
    that.aggregateByDate       = aggregateByDate;
    that.aggregateByInitiative = aggregateByInitiative;

    //return the object with its public methods and attributes
    return that;


}

module.exports = EventManager;