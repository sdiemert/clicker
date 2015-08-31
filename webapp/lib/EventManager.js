/**
 * Created by sdiemert on 15-08-30
 */

function EventManager(proc) {

    proc = proc || {};

    var that = {};

    that.publicAttr = "123"; //a public attribute

    proc.protectedAttr = "abc"; //a protected attribute

    var publicMethod = function () {

        //implement public method here...

    }

    var protectedMethod = function () {

        //implement protected method here...

    }

    var privateMethod = function () {

        //implement a private method here...

    }

    //link protected methods here...
    proc.protectedMethod = protectedMethod;

    //link public methods here...
    that.publicMethod = publicMethod;

    //return the object with its public methods and attributes
    return that;


}

module.exports = EventManager;