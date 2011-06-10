#!/usr/bin/env python
# -*- coding: utf-8 -*-


#===============================================================================
# DOCS
#===============================================================================

"""Module for scan files in a folder/s

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
__version__ = "0.2"
__date__ = "2010/12/22"
__license__ = "lgpl 3"


#===============================================================================
# IMPORTS
#===============================================================================

import os


#===============================================================================
# CLASSES
#===============================================================================

class ResourceDirs(object):

    def __init__(self, paths, exts=None):
        """Create a new instance

        @param path: path or a list of path to directory.
        @param exts: A list or tuple of valid extensions or None

        """
        if isinstance(paths, basestring):
            self._paths = (paths,)
        elif isinstance(paths, (list, tuple)):
            self._paths = paths
        else:
            msg = "'paths' must be string, unicode list or tuple instance, find %s"
            raise TypeError(msg % str(type(paths)))
        
        if isinstance(exts, basestring):
            self._exts = (exts,)
        elif isinstance(paths, (list, tuple)):
            self._exts = exts
        elif exts == None:
            self._exts = ()
        else:
            msg = "'exts' must be string, unicode list or tuple instance or None, find %s"
            raise TypeError(msg % str(type(paths)))
        self._resources = {}
        self.rescan()

    def rescan(self):
        """Reload the 'path'"""
        self.clear()
        for p in self._paths:
            for dir_path, _, filenames in os.walk(p):
                for filename in filenames:
                    if self._exts:
                        ext = (filename.rsplit(".", 1)[1]).lower() \
                               if "." in filename \
                               else filename
                        if ext in self._exts:
                            self._resources[filename] = os.path.join(dir_path,
                                                                     filename)
                    else:
                        self._resources[filename] = os.path.join(dir_path,
                                                                 filename)
                break

    def clear(self):
        self._resources.clear()
        
    def get(self, k, d=None):
        return self._resources.get(k, d)
    
    def __getitem__(self, k):
        return self._resources[k]

    def __repr__(self):
        return "<%s %s %s>" % (self.__class__.__name__,
                               str(self._paths),
                               hex(id(self)))

    @property
    def paths(self):
        """The path of the ResourceDict"""
        return self._paths

    @property
    def exts(self):
        """The valid extensions of the resources"""
        return self._exts

    @property
    def resources(self):
        """"The list of existing resources"""
        return self._resources.keys()


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
