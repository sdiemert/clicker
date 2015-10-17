/**
 * Created by sdiemert on 15-08-30.
 */

var User = require("./models/User").User;
var util   = require('util');

function UserManager(proc) {

    proc = proc || {};

    var that = {};


    /**
     * Gets information about all of the members.
     *
     * @throws {Error} if the next argument is not a valid function.
     *
     * @param pattern {String} - matches on the name field of the user's collection in mongo, defaults to '.*' if null.
     * @param next {Function} - callback function, has signature: function(String, Array)
     *
     * @return {Array} - of user objects from the database.
     */
    var getUsers = function (pattern, next) {

        if(!next || typeof next !== 'function' || next.length !== 2){
            throw new Error("UserManager.getUser(String, Function) expects second argument to be a function with arity 2.");
        }

        //default pattern matches everything.
        pattern = pattern || ".*";


        User.find({
            name: {$regex: pattern, $options: 'g'}
        }).exec(function (err, results) {

            if (err) {
                return next(err, null);
            }

            return next(null, results);

        });

    };


    that.getUsers = getUsers;

    return that;

}

module.exports = UserManager;
