.. author: Alan Chen

Installation
============

Make sure your Python version is 2.7.x.

Setting up Virtual Environment
------------------------------

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

	$ python manage.py create_table

Downloading Demo Models
-----------------------

Since our trained models contain intermediate data that allows you to train it further with new corpora, their sizes are larger than the size GitHub LFS is willing to handle.

To download the demo models, in the ``trained`` folder, run:

::
	$ cd trained
	$ python download.py

For detailed change log of our trained model, see ``trained/README.md``.

All the files are available `HERE <https://drive.google.com/drive/folders/0B28rFtb9-7L7SzRFY19pNVVidG8?usp=sharing>`_.

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
