

# Key: pkg to import
# value: the page to get help about install the package
NON_EASY_INSTALLABLES = {
    "PyQt4": "http://www.riverbankcomputing.co.uk/software/pyqt/intro", }

DEPENDENCIES = ("numpy", "python-graph-core", "python-graph-dot", "lxml")


#===============================================================================
# VALIDATE THE NEEDED MODULES
#===============================================================================

for mn, urlm in NON_EASY_INSTALLABLES.items():
    try:
        __import__(mn)
    except ImportError:
        msg = "Module '%s' not found. For more details see '%s'.\n" % (mn, urlm)
        raise Exception(msg)
