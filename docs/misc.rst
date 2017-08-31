.. author: Alan Chen

Miscellaneous
=============

This page documents some miscellaneous setup regarding Findmyreviewers.

Travis CI
---------

Due to our time constraint, Findmyreviewers does not have a complete testing suite yet.
But at least Travis CI can help us to see if Findmyreviewers can be configurated correctly in a fresh and clean environment.

To setup Travis CI, you need to specify all the settings in the ``.travis.yml`` file in the root directory of the project.
For Findmyreviewers, we tell Travis CI to follow our :ref:`Installation` guide and test if the web server is running without problem.

Go to `Travis CI <https://travis-ci.org/>`_ and login with your Github account. Simply turn on Travis CI for your repository and you are good to go.

Codacy
------

Codacy is a code quality checker that can help you to evaluate your code quality and point out potential problems.

Go to `Codacy <https://www.codacy.com>`_ and sign up with your Github account, turn it on for your repository, and you are good to go!