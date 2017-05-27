django_project
==============

Project Description

This project was put together in a couple hours as a proof of concept for 
web app that enables students to find study buddies.

See screenshots in /screenshots :) 

TODO:
* Update fab automation tools (fabric.py)

* Create REST API, using Django Restframework
* Add Social Auth (Facebook, Google, LinkedIn)
* Finanlize User Registeration and Profile backend modules
* Finish Matching Backend
* Revamp front end, maybe use React / Angular
* Deploy app to AWS or GCP & dockerize app


Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ py.test

Running the server in development
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

python manage.py runserver 0.0.0.0:<port>



Deployment
----------

The following details how to deploy this application.

* Clone this repository
* Install system and python (pip) dependencies 
* Install bower / js dependencies in study_buddy/static/vendors/
* Setup DB (default is sqlite) and run migrations via django manage




