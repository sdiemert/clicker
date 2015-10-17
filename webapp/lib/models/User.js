var mongoose = require("mongoose");

var userSchema = mongoose.Schema({
    _id : String,
    name : String,
    pageContent : String
}, {
    collection : "users"
});

var Member = mongoose.model("User", userSchema, "users");

module.exports = {User : User};