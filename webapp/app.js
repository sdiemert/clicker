var express        = require('express');
var expressSession = require('express-session');
var path           = require('path');
var favicon        = require('serve-favicon');
var logger         = require('morgan');
var cookieParser   = require('cookie-parser');
var bodyParser     = require('body-parser');
var mongoose       = require('mongoose');

var routes      = require('./routes/index');
var members     = require('./routes/members');
var status      = require('./routes/status');
var initiatives = require('./routes/initiatives');
var downloads   = require('./routes/downloads');
var users       = require('./routes/user');
var admin       = require('./routes/admin');

process.env.MONGO = process.env.MONGO || "localhost:27017";

var app = express();

mongoose.connect(process.env.MONGO + "/sparc");

var conn = mongoose.connection;

conn.on('error', function (x) {

    console.log("Cound not connect to MongoDB, error: " + x);
    console.log("Cannot run without db connection, exiting...");

    //we can't run the app without a db connection...
    // exit the program.
    process.exit();

});

conn.once('open', function () {

    console.log("Connected to Mongo database!");

});

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'hbs');
require('hbs').registerPartials(path.join(__dirname, 'views/partials'));
require('hbs').registerHelper('json', function (data) {
    return JSON.stringify(data);
});

/**
 * Helper for casting names to HTML id's for easy manipulation in browser.
 */
require('hbs').registerHelper('makeId', function (data) {
    data = data.replace(" ", "-");
    data = data.toLowerCase();

    return data;

});

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(cookieParser());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use(expressSession({
        secret           : 'superSecret',
        resave           : true
    }
));
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', routes);
app.use('/members', members);
app.use('/status', status);
app.use('/initiatives', initiatives);
app.use('/downloads', downloads);
app.use('/users', users);
app.use('/admin', admin);

// catch 404 and forward to error handler
app.use(function (req, res, next) {
    var err    = new Error('Not Found');
    err.status = 404;
    next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    app.use(function (err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error  : err
        });
    });
}

// production error handler
// no stacktraces leaked to user
app.use(function (err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error  : {}
    });
});


module.exports = app;
