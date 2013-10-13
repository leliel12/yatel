#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""Functionality for create and execute
`ETLs <http://en.wikipedia.org/wiki/Extract,_transform,_load>`_

"""


#===============================================================================
# INSPECT
#===============================================================================

import inspect
import abc
import string
import inspect
import os
import imp
import sys
import re

from yatel import db
from yatel import dom


#===============================================================================
# CONSTANTS
#===============================================================================

#: Template for create etl files
ETL_TEMPLATE = string.Template("""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''auto created template for create your custom etl for yatel'''


from yatel import etl, dom


#===============================================================================
# PUT YOUT ETLs HERE
#===============================================================================

class CustomETL(etl.ETL):

    # you can access the current network from the attribute 'self.nw'

${code}

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

""".strip())

#===============================================================================
# META CLASSES
#===============================================================================

class _ETLMeta(abc.ABCMeta):
    """Metaclass for control the ETL inheritance

    """
    def __init__(self, *args, **kwargs):
        super(_ETLMeta, self).__init__(*args, **kwargs)
        spec = inspect.getargspec(self.setup)
        if spec.varargs or spec.keywords or spec.defaults:
            msg = "Only positional arguments without defauls is alowed on setup"
            raise TypeError(msg)
        self.setup_args = tuple(arg for arg in spec.args if arg != "self")


#===============================================================================
# CLASSES
#===============================================================================

class ETL(object):

    __metaclass__ = _ETLMeta

    def setup(self):
        pass

    def pre_haplotype_gen(self):
        pass

    @abc.abstractmethod
    def haplotype_gen(self):
        return []

    def post_haplotype_gen(self):
        pass

    def pre_fact_gen(self):
        pass

    @abc.abstractmethod
    def fact_gen(self):
        return []

    def post_fact_gen(self):
        pass

    def pre_edge_gen(self):
        pass

    @abc.abstractmethod
    def edge_gen(self):
        return []

    def post_edge_gen(self):
        pass

    def teardown(self):
        pass


#===============================================================================
# FUNCTIONS
#===============================================================================

def scan_dir(dirpath):
    """Retrieve all python files from a given directory"""
    dir_found = {}
    for content in os.listdir(dirpath):
        path = os.path.join(dirpath, content)
        if os.path.isfile(path) and not content.startswith(".") \
           and not content.startswith("_") \
           and re.match(r"^.*[.]py.?$", content):
            etl_found = scan_file(path)
            if etl_found:
                dir_found[path] = etl_found
    return dir_found


def scan_file(filepath):
    """Retrieve all yatel.etl.ETL subclass of a given file"""
    dirname, filename = os.path.split(filepath)
    modname = os.path.splitext(filename)[0]
    etlmodule = None
    etlfound = {}
    if modname not in sys.modules:
        found = imp.find_module(modname, [dirname])
        etlmodule = imp.load_module(modname, *found)
    else:
        etlmodule = sys.modules[modname]
    for k, v in vars(etlmodule).items():
        if not k.startswith("_") and inspect.isclass(v) and issubclass(v, ETL):
            etlfound[k] = v
    if not etlfound:
        del sys.modules[modname]
    return etlfound


def etlcls_from_module(filepath, clsname):
    """Return a class of a given  filepath.

    """
    return scan_file(filepath)[clsname]


def get_template():
    defs = []
    for amethod in ETL.__abstractmethods__:
        defd = ("    def {}(self):\n"
                "        raise NotImplementedError()\n").format(amethod)
        defs.append(defd)
    return ETL_TEMPLATE.substitute(code="\n".join(defs))


def execute(nw, etl, *args):
    """Execute an ETL instance.
    """

    etl_name = type(etl).__name__

    if not isinstance(etl, ETL):
        msg = "etl is not instance of a subclass of yatel.etl.ETL"
        raise TypeError(msg)

    etl.setup(*args)

    etl.pre_haplotype_gen()
    for hap in etl.haplotype_gen() or []:
        if isinstance(hap, dom.Haplotype):
            nw.add_element(hap)
        else:
            msg = ("ETL '{}' is 'haplotype_gen' method"
                   "return  a non 'dom.Haplotype' object").format(etl_name)
            raise TypeError(msg)
    etl.post_haplotype_gen()

    etl.pre_fact_gen()
    for fact in etl.fact_gen() or []:
        if isinstance(fact, dom.Fact):
            nw.add_element(fact)
        else:
            msg = ("ETL '{}' 'fact_gen' method"
                   "return  a non 'dom.Fact' object").format(etl_name)
            raise TypeError(msg)
    etl.post_fact_gen()

    etl.pre_edge_gen()
    for edge in etl.edge_gen() or []:
        if isinstance(edge, dom.Edge):
            nw.add_element(edge)
        else:
            msg = ("ETL '{}' 'edge_gen' method"
                   "return a non 'dom.Edge' object").format(etl_name)
            raise TypeError(msg)
    etl.post_edge_gen()

    etl.teardown()


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

