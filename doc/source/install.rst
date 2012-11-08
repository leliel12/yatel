==================
Installation Guide
==================

Ubuntu/Debian/Mint
------------------

1. Execute

    .. code-block:: bash

            $ sudo apt-get install python-setuptools python-pip python-qt4
              python-qt4-gl python-qt4-phonon build-essential python-dev swig
              subversion python-numpy python-qscintilla2 python-sip

.. _box2d:

2. Next install box2d

    .. code-block:: bash

        $ svn checkout http://pybox2d.googlecode.com/svn/trunk/ pybox2d
        $ cd pybox2d
        $ python setup.py build
        $ sudo python setup.py install

3. **Optional** GraphTool

    This lib is used only on module ``yatel.conversors.graph_tool2yatel``
    The instalation notes are here:

        http://projects.skewed.de/graph-tool/wiki/GraphToolDownload#DebianandUbuntu

4. Finally

    .. code-block:: bash

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
    - PyBox2d http://pybox2d.googlecode.com (in linux see box2d_)
    - GraphTool http://projects.skewed.de/graph-tool/wiki/GraphToolDownload
      (For use ``yatel.conversors.graph_tool2yatel``)
    - **ONLY IN WINDOWS** PyReadLine http://pypi.python.org/pypi/pyreadline

Finally open a console and execute

    .. code-block:: bat

        > easy_install yatel





