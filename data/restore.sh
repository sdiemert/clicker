#!/bin/bash

mongorestore --collection events --db sparc events.bson
mongorestore --collection tags --db sparc tags.bson
mongorestore --collection initiatives --db sparc initiatives.bson
mongorestore --collection members --db sparc members.bson
