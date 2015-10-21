var mongoose = require("mongoose");

var memberSchema = mongoose.Schema({
    id : String,
    name : String,
    city : String,
    province : String
}, {
    collection : "members"
});

var Member = mongoose.model("Member", memberSchema, "members");

module.exports = {Member : Member};