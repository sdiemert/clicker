var mongoose = require("mongoose");

var initSchema = mongoose.Schema({
    _id : String,
    name : String
}, {
    collection : "initiatives"
});

var Init = mongoose.model("Initiative", initSchema, "initiatives");

module.exports = {Initiative : Init};