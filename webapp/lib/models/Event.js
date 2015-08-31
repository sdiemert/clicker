var mongoose = require("mongoose");

var eventSchema = mongoose.Schema({
    _id : String,
    tag : String,
    member : String,
    time : Number
}, {
    collection : "events"
});

var Event = mongoose.model("Event", eventSchema, "events");

module.exports = {Event : Event};