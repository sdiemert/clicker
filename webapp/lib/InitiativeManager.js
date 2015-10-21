/**
 * Created by sdiemert on 15-08-30.
 */

var Initiative = require("./models/Initiative").Initiative;
var Tag        = require("./models/Tag").Tag;
var util       = require('util');
var async      = require('async');

function InitiativeManager(proc) {

    proc = proc || {};

    var that = {};


    /**
     * Gets information about all of the current Initiatives
     *
     * @throws {Error} if the next argument is not a valid function.
     *
     * @param pattern {String} - matches on the _id field of the initiatives's collection in mongo, defaults to '.*' if null.
     * @param next {Function} - callback function, has signature: function(String, Array)
     *
     * @return {Array} - of member objects from the database.
     */
    var getInits = function (pattern, next) {

        if (!next || typeof next !== 'function' || next.length !== 2) {
            throw new Error("InitiativeManager.getInitiative(String, Function) expects second argument to be a function with arity 2.");
        }

        //default pattern matches everything.
        pattern = pattern || ".*";

        var toReturn = {};

        Initiative.find({
            _id: {$regex: pattern, $options: 'g'}
        }).exec(function (err, inits) {

            if (err) {
                console.log(err);
                return next(err, null);
            } else {

                async.each(
                    inits,
                    function (i, cb) {

                        toReturn[i._id] = {name: i.name, tags: []};

                        Tag.find({
                            initiative: {$regex: i._id, $options: 'g'}
                        }).exec(function (err, r) {
                            if (err) {
                                cb(err);
                            } else {

                                for (var x in r) {

                                    toReturn[i._id].tags.push(r[x])

                                }

                                cb(null);
                            }
                        })

                    }, function (err) {

                        if (err) {
                            console.log(err);
                            return next(err, null);
                        } else {
                            return next(err, toReturn)
                        }

                    }
                )

            }

        });

    };

    var make_id = function (x) {
        x = x.replace(" ", "_");
        return x.toLowerCase();
    };

    var addInit = function (name, tags, next) {

        console.log(tags);

        Initiative.update(
            {_id: make_id(name), name: name},
            {},
            {upsert: true}
        ).exec(function (err, result_i) {

            if (err) {
                console.log(err);
                return next(err);
            } else {
                async.each(
                    tags,
                    function (t, done) {

                        Tag.update(
                            {_id: make_id(t), initiative: make_id(name), name: t},
                            {},
                            {upsert: true}
                        ).exec(
                            function (err, result_t) {
                                return done(err);
                            }
                        );

                    }, function (err) {
                        return next(err);
                    }
                );

            }

        })

    };


    that.addInit  = addInit;
    that.getInits = getInits;

    return that;

}

module.exports = InitiativeManager;
