#!/usr/bin/env python
# -*- coding: utf-8 -*-

# resdir.py

#===============================================================================
# DOCS
#===============================================================================

"""Module for scan files in a folder

    Example:

        >>> import resdir
        >>> img = resdir.ResourceDir("/home/juan/img", ["jpg", "png"])
        >>> img["myfile.png"]
        /home/juan/img/myfile.png
        >>> img.get("myfile.exe", "not found") # exe file not in extensions
        "not found"

"""

#===============================================================================
# META
#===============================================================================

__author__ = "JBC <jbc dot develop at gmail dot com>"
__version__ = "0.1"
__date__ = "2010/11/27"
__license__ = "lgpl 3"

#===============================================================================
# IMPORTS
#===============================================================================

import os

#===============================================================================
# CLASSES
#===============================================================================

class ResourceDir(dict):

    def __init__(self, path, exts=None):
        """Create a new instance

        @param path: Path to directory.
        @param exts: A list or tuple of valid extensions or None

        """
        assert isinstance(path, basestring) and os.path.isdir(path)
        assert isinstance(exts, (list, tuple)) or exts == None
        self._path = path
        self._exts = exts or []
        self.rescan()

    def rescan(self):
        """Reload the 'path'"""
        self.clear()
        for dir_path, _, filenames in os.walk(self._path):
            for filename in filenames:
                if self._exts:
                    ext = (filename.rsplit(".", 1)[1]).lower() \
                           if "." in filename \
                           else filename
                    if ext in self._exts:
                        self[filename] = os.path.join(dir_path, filename)
                else:
                    self[filename] = os.path.join(dir_path, filename)
            break

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "<%s (%s) %s>" % (self.__class__.__name__,
                                 self._path,
                                 hex(id(self)))

    @property
    def path(self):
        """The path of the ResourceDict"""
        return self._path

    @property
    def exts(self):
        """The valid extensions of the resources"""
        return self._exts

    @property
    def resources(self):
        """"The list of existing resources"""
        return self.keys()


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
