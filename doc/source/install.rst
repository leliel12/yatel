==================
Installation Guide
==================

Ubuntu/Debian/Mint
------------------

1. Execute

    .. code-block:: bash

            $ sudo apt-get install python-setuptools python-pip python-qt4
              swig subversion python-numpy python-sip

2. **Optional** GraphTool

    This lib is used only on module ``yatel.conversors.graph_tool2yatel``
    The instalation notes are here:

        http://projects.skewed.de/graph-tool/wiki/GraphToolDownload#DebianandUbuntu

3. Finally

    .. code-block:: bash

            $ sudo pip install yatel


Windows or other *nix
---------------------

    - Python 2.7 http://www.python.org
    - Setup tools http://pypi.python.org/pypi/setuptools
    - Mercurial (if you install yatel from the repo) http://mercurial.selenic.com/
    - PyQt4 http://www.riverbankcomputing.co.uk/software/pyqt
    - Sip http://www.riverbankcomputing.co.uk/software/sip
    - NumPy http://numpy.scipy.org/
    - GraphTool http://projects.skewed.de/graph-tool/wiki/GraphToolDownload
      (For use ``yatel.conversors.graph_tool2yatel``)
    - **ONLY IN WINDOWS** PyReadLine http://pypi.python.org/pypi/pyreadline

Finally open a console and execute

    .. code-block:: bat

        > easy_install yatel


From repo
---------

First install all dependencies, and then

    .. code-block:: bash

        $ hg clone http://bitbucket.org/leliel12/yatel yatel
        $ cd yatel
        $ python setup.py install





