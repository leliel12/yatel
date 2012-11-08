==================
Installation Guide
==================

Ubuntu/Debian/Mint
------------------

#. Execute

    ::
        sudo apt-get install python-setuptools python-pip python-qt4
        python-qt4-gl python-qt4-phonon build-essential python-dev swig
        subversion python-numpy python-qscintilla2 python-sip


#. Next install box2d

.. code-block:: bash

    $ svn checkout http://pybox2d.googlecode.com/svn/trunk/ pybox2d
    $ cd pybox2d
    $ python setup.py build
    $ sudo python setup.py install

#. Finally

    ::
        $ sudo pip install yatel


Windows or other *nix
---------------------

    - Python 2.7 http://www.python.org
    - Setup tools http://pypi.python.org/pypi/setuptools
    - SVN (For box2d) http://subversion.tigris.org/
    - Mercurial (if you install yatel from the repo) http://mercurial.selenic.com/
    - PyQt4 http://www.riverbankcomputing.co.uk/software/pyqt
    - QScintilla 2 http://www.riverbankcomputing.co.uk/software/qscintilla
    - Sip http://www.riverbankcomputing.co.uk/software/sip
    - NumPy http://numpy.scipy.org/
    - **ONLY IN WINDOWS** http://pypi.python.org/pypi/pyreadline
    - **ONLY IN WINDOWS** http://pybox2d.googlecode.com

Finally open a console and execute

::
    easy_install yatel





