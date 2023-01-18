# chat13
Simple chat server created as educational project.

Installation
-
At first you need to create and activate virtual environment

    $ python -m venv venv
    $ source venv/bin/activate

Then you need to install dependecies. WARNING: This step requieres C compiler and build tools to compile uWSGI

    $ pip install requirements.txt

Now create and upgrade database

    $ flask db upgrade

Now you need to create rooms for chating.
Some example room names are listed in the file make_room.py, but if you want more or different rooms,
you can edit this file. More instructions are in the comments in this file

    $ python make_room.py

To use https you need certificate.
Generate one yourself and get real certificate from CA

Usage
-
Before running this app, you should change SECRET_KEY variable in the app/config.py file
or export it in your shell

    $ eport SECRET_KEY='some-strong-and-secret-value'

Now you can run this app

    $ uwsgi --ini conf.ini

Advanced design patterns
-
This project was started as exercise for IT course, to put as many Advanced design pattern as possible in it.
When this course finished, they were:
* Model-View-Comtroller
* Active Record: data models are stored in app/models.py, they include some methods used by application logic
* Identity Field: id fields of data models
* Foreign Key Mapping: Post table has id keys of User and Room tables
* Transaction Script: Domain logic is mostly functions in app/routes.py and app/models.py called by webpage
* Page Controller: Each route in app/routes.py is a controller for one webpage
* Service Layer: Routes in app/routes.py are services for webpage loaded on remote machines
* Template View: Templates sre stored in app/templates/ directory; functions in app/routes.py use them to render webpages
* Client Session State: Session is stored at user's computer as signed cookie file
* Data Transfer Object: Each request has message and user session data
