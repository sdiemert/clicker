var mongoose = require("mongoose");

var eventSchema = new mongoose.Schema({
    tag : String,
    member : String,
    time : Number,
    initiative: String,
    user : {type:String, default: null}
}, {
    collection : "events"
});

var Event = mongoose.model("Event", eventSchema, "events");

module.exports = {Event : Event};