==================
Installation Guide
==================

Ubuntu/Debian/Mint
^^^^^^^^^^^^^^^^^^

Execute

.. code-block:: bash

    $ apt-get install python-dev libatlas-base-dev gfortran
    $ pip install yatel

Development version

.. code-block:: bash

    $ pip install --pre yatel


Windows or other xnix
^^^^^^^^^^^^^^^^^^^^^

- Python 2.7 http://www.python.org
- Setup tools http://pypi.python.org/pypi/setuptools
- Mercurial (if you install yatel from the repo) http://mercurial.selenic.com/
- Scipy http://scipy.org/scipylib/index.html
- NumPy http://numpy.scipy.org/


Finally open a console and execute

.. code-block:: bat

    > easy_install pip
    > pip install yatel

For development version

.. code-block:: bat

    > pip install --pre yatel

From repo
^^^^^^^^^

First install all dependencies, and then

.. code-block:: bash

    $ hg clone http://bitbucket.org/yatel/yatel yatel
    $ cd yatel
    $ python setup.py sdist
    $ pip install dist/yatel-<VERSION>.tar.gz


Install as develop
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ hg clone http://bitbucket.org/yatel/yatel yatel
    $ cd yatel
    $ pip install -r requirements.txt
    $ python setup.py develp



