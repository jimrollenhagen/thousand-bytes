Thousand Bytes
==============

A REST API written in Python to convert image files to ascii art.

Running the app
---------------

* Make sure tox is installed - `sudo pip install tox`. In my experience, tox
  prefers to be globally installed, but may work fine from a virtualenv.
* Run `tox -e run` - this will start the API server locally in debug mode.

Running tests
-------------

* Make sure tox is installed - `sudo pip install tox`. In my experience, tox
  prefers to be globally installed, but may work fine from a virtualenv.
* Run `tox` - this will run tests on both Python 2.7 and 3.5, if they are
  installed. It will also run `flake8` to lint the code.
* `tox -e $env` can be run to limit to a single set of tests, depending on
  the value of `$env`:
  * `py27`: run tests on Python 2.7.
  * `py35`: run tests on Python 3.5
  * `pep8`: run the linter.

API usage
---------

There is one API call at `POST /ascii`. It accepts multipart form data with
the following parameters:

* `image`: the image to be converted.
* `height`: optional positive integer, the height in lines of the resulting
  ascii art. Defaults to 50.

Example usage
-------------

Convert an image with default height::

    curl -F image=@images/world-map.png http://localhost:5000/ascii

Convert an image with height of 30::

    curl -F height=30 -F image=@images/world-map.png http://localhost:5000/ascii

Dependencies
------------

Dependencies are specified in requirements.txt and test-requirements.txt.

flask, flake8, and nose are extremely reliable dependencies used widely by the
Python community.

asciimatics is a library built to enable developers to create console UIs,
and not necessarily designed for a tool like this. It appears to be healthy
and well-maintained. It supports Python 2.7 and 3.5, and is well-documented.
However, the `ImageFile` class we use in this application is not documented
(though easy to understand by reading the code). It isn't marked as an internal
API via the usual Python conventions, but to hedge against this class changing
from under us, we pin it to `<2.0.0`. It does appear to be the best choice in
the community for this task, and it is licensed under the Apache 2.0 License.
This enables us to lift the code out later if the library is later found to
be unstable or unsuitable.

Known issues
------------

None.
