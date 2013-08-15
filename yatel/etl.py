#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""

"""


#===============================================================================
# INSPECT
#===============================================================================

import string
import inspect
import abc


#===============================================================================
# CONSTANTS
#===============================================================================

CLEAR_MODE = "clear"
APPEND_MODE = "append"

MODES = (CLEAR_MODE, APPEND_MODE)

ETL_TEMPLATE = string.Template("""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''auto created template for create your custom etl for yatel'''


from yatel import etl


#===============================================================================
# PUT YOUT ETLs HERE
#===============================================================================

class CustomETL(etl.ETL):

${code}

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

""".strip())


#===============================================================================
# CLASSES
#===============================================================================

class ETL(object):

    __metaclass__ = abc.ABCMeta

    def setup(self):
        pass

    @abc.abstractmethod
    def get_mode(self):
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

def get_template():
    defs = []
    for amethod in ETL.__abstractmethods__:
        defd = ("    def {}(self):\n"
                "        raise NotImplementedError()\n").format(amethod)
        defs.append(defd)
    return ETL_TEMPLATE.substitute(code="\n".join(defs))


def execute_etl(nw, etlcls):

    etl_name = type(etlcls).__name__

    if not inspect.isclass(etlcls) or not issubclass(etlcls, ETL):
        msg = "'{}' is not subclass of ETL".format(etlname)
        raise TypeError(msg)

    etl = etlcls()
    etl.setup()
    mode = etl.get_mode()

    if not nw.created:
        new_nw = db.YatelNetwork(db.parse_uri(nw.uri), create=True, log=True)

        if mode not in MODES:
            msg = "Invalid mode '{}'".format(str(mode))
            raise ValueError(msg)
        elif mode == CLEAR_MODE:
            pass
        elif mode == APPEND_MODE:
            new_nw.add_elements(nw.haplotype_iterator())
            new_nw.add_elements(nw.fact_iterator())
            new_nw.add_elements(nw.edge_iterator())
            new_nw.add_elements(nw.version_iterator())

        nw.delete_tables()
        nw = new_nw

    etl.pre_haplotype_gen()
    for hap in etl.haplotype_gen():
        if isinstance(hap, dom.Haplotype):
            nw.add_element(hap)
        else:
            msg = ("ETL '{}' is 'haplotype_gen' method"
                   "return  a non 'dom.Haplotype' object").format(etl_name)
            raise TypeError(msg)
    etl.post_haplotype_gen()

    etl.pre_fact_gen()
    for fact in etl.fact_gen():
        if isinstance(fact, dom.Fact):
            nw.add_element(fact)
        else:
            msg = ("ETL '{}' is 'fact_gen' method"
                   "return  a non 'dom.Fact' object").format(etl_name)
            raise TypeError(msg)
    etl.post_fact_gen()

    etl.pre_edge_gen()
    for edge in etl.edge_gen():
        if isinstance(hap, dom.Edge):
            nw.add_element(hap)
        else:
            msg = ("ETL '{}' is 'edge_gen' method"
                   "return  a non 'dom.Edge' object").format(etl_name)
            raise TypeError(msg)
    etl.post_edge_gen()

    etl.teardown()

    nw.end_creation()


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

