/**
 * Created by sdiemert on 15-08-30.
 */

var Member = require("./models/Member").Member;
var util   = require('util');

function MemberManager(proc) {

    proc = proc || {};

    var that = {};


    /**
     * Gets information about all of the members.
     *
     * @throws {Error} if the next argument is not a valid function.
     *
     * @param pattern {String} - matches on the id field of the member's collection in mongo, defaults to '.*' if null.
     * @param next {Function} - callback function, has signature: function(String, Array)
     *
     * @return {Array} - of member objects from the database.
     */
    var getMembers = function (pattern, next) {

        if(!next || typeof next !== 'function' || next.length !== 2){
            throw new Error("MemberManager.getMembers(String, Function) expects second argument to be a function with arity 2.");
        }

        //default pattern matches everything.
        pattern = pattern || ".*";


        Member.find({
            id: {$regex: pattern, $options: 'g'}
        }).exec(function (err, results) {

            if (err) {
                return next(err, null);
            }

            return next(null, results);

        });

    };


    that.getMembers = getMembers;

    return that;

}

module.exports = MemberManager;
