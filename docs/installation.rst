.. author: Alan Chen

Installation
============

Make sure your Python version is 2.7.x.

Setup Environment
-----------------

Using ``virtualenv`` is highly recommended.

If you do not have a virtual environment yet in the project folder, set
it up with:

::

    $ virtualenv venv

Activate the virtual environment:

::

    $ source venv/bin/activate

Install required packages:

::

    $ pip install -r requirements.txt

Initialize the tables in the web app database:

::

	$ python manage.py createtable

Running the Server
------------------

::

    $ python manage.py runserver

Then after navigate to the following address:

::

    127.0.0.1:5000

To access the dashboard, please visit:

::

    127.0.0.1:5000/dashboard
