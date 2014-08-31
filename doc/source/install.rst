==================
Installation Guide
==================

Ubuntu/Debian/Mint
------------------

Execute

.. code-block:: bash

    $ sudo apt-get install python-dev libatlas-base-dev gfortran
    $ sudo pip install yatel



Windows or other Xnix
---------------------

- Python 2.7 http://www.python.org
- Setup tools http://pypi.python.org/pypi/setuptools
- Mercurial (if you install yatel from the repo) http://mercurial.selenic.com/
- Scipy http://scipy.org/scipylib/index.html
- NumPy http://numpy.scipy.org/


Finally open a console and execute

.. code-block:: bat

    > easy_install pip
    > pip install yatel


From repo
---------

First install all dependencies, and then

.. code-block:: bash

    $ hg clone http://bitbucket.org/yatel/yatel yatel
    $ cd yatel
    $ python setup.py sdist
    $ pip install dist/yatel-<VERSION>.tar.gz





