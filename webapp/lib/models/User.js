var mongoose = require("mongoose");

var userSchema = mongoose.Schema({
    id : String,
    name : String,
    pageContent : String,
    admin : Boolean,
    password : String
}, {
    collection : "users"
});

var User = mongoose.model("User", userSchema, "users");

module.exports = {User : User};