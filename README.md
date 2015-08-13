# Clicker

This project is a full-stack clicker application. An arduino acts as an data sensor, users can click buttons on the arduino and it will track each click. The arduino's clicker data can be downloaded to a client application on the users PC (supports both Windows and OSX). The client application allows the user to upload their clicker data to the cloud. A web application aggregates and presents the data from multiple clickers. 

## Project Structure

This project has three main directories: 

* `embedded/` : contains code for an arduino that is used to collect clicker data.
* `client/` : a python application to communicate wit the arduino clicker device and upload the data to the web application
* `webapp/` : (coming soon) the web application that will aggregate, store, and present data from multiple clickers. 

Each sub directory has a README.md file that contains details of the specific component.

## Developers

Interested in contributing? Please contact me via the GitHub messaging system. 
