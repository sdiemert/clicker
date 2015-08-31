var mongoose = require("mongoose");

var eventSchema = new mongoose.Schema({
    _id : String,
    tag : String,
    member : String,
    time : Number,
    initiative: String,
    user : {type : mongoose.Schema.Types.ObjectId, default: null}
}, {
    collection : "events"
});

var Event = mongoose.model("Event", eventSchema, "events");

module.exports = {Event : Event};