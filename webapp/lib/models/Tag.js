var mongoose = require("mongoose");

var tagSchema = mongoose.Schema({
    _id : String,
    name : String,
    initiative : String
}, {
    collection : "tags"
});

var Tag = mongoose.model("Tag", tagSchema, "tags");

module.exports = {Tag : Tag};