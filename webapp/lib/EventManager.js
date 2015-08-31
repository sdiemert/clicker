/**
 * Created by sdiemert on 15-08-30
 */

var Event = require("./models/Event").Event;

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

            if(err){
                console.log(err);
                return next(err, null);
            }else{
                return next(null, result);
            }

        });

    };

    that.getEvents = getEvents;

    //return the object with its public methods and attributes
    return that;


}

module.exports = EventManager;