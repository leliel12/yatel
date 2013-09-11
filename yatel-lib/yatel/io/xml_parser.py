#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 'THE WISKEY-WARE LICENSE':
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

'''This module is used for construct yatel.dom object using yatel xml format
files

'''

#===============================================================================
# IMPORTS
#===============================================================================

from xml.sax import saxutils

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from yatel import dom
from yatel.io import core


#===============================================================================
# IO FUNCTIONS
#===============================================================================

class XMLParser(core.BaseParser):

    def start_elem(self, tag, attrs={}):
        attrs = ' '.join(['{}={}'.format(k, saxutils.quoteattr(v))
                                           for k, v in attrs.items()])
        return u'<{tag} {attrs}>'.format(tag=tag, attrs=attrs)

    def end_elem(self, tag):
        return '</{tag}>'.format(tag=tag)

    def to_content(self, data):
        return saxutils.escape(str(data))

    def dump(self, nw, stream=None, **kwargs):
        self.validate_read(nw)

        fp = stream or StringIO.StringIO()
        hap_types = nw.haplotype_attributes_types()
        fact_types = nw.fact_attributes_types()
        hap_id_type = hap_types["hap_id"]

        fp.write(self.start_elem("network",
                                 {"version": core.DEFAULT_VERSION}))

        fp.write(self.start_elem("types"))
        fp.write(self.start_elem("haplotypes"))
        for k, v in self.types2strdict(hap_types).items():
            fp.write(self.start_elem("type", {"name": k}))
            fp.write(self.to_content(v))
            fp.write(self.end_elem("type"))
        fp.write(self.end_elem("haplotypes"))

        fp.write(self.start_elem("facts"))
        for k, v in self.types2strdict(fact_types).items():
            fp.write(self.start_elem("type", {"name": k}))
            fp.write(self.to_content(v))
            fp.write(self.end_elem("type"))
        fp.write(self.end_elem("facts"))
        fp.write(self.end_elem("types"))

        fp.write(self.start_elem("haplotypes"))
        for hap in nw.haplotypes_iterator():
            fp.write(self.start_elem("haplotype"))
            hapd = self.hap2dict(hap, hap_id_type, hap_types)
            for k, v in hapd.items():
                fp.write(self.start_elem("attribute", {"name": k}))
                fp.write(self.to_content(v))
                fp.write(self.end_elem("attribute"))
            fp.write(self.end_elem("haplotype"))
        fp.write(self.end_elem("haplotypes"))

        fp.write(self.start_elem("facts"))
        for fact in nw.facts_iterator():
            fp.write(self.start_elem("fact"))
            factd = self.fact2dict(fact, hap_id_type, fact_types)
            for k, v in factd.items():
                fp.write(self.start_elem("attribute", {"name": k}))
                fp.write(self.to_content(v))
                fp.write(self.end_elem("attribute"))
            fp.write(self.end_elem("fact"))
        fp.write(self.end_elem("facts"))

        fp.write(self.start_elem("edges"))
        for edge in nw.edges_iterator():
            fp.write(self.start_elem("edge"))
            edged = self.edge2dict(edge, hap_id_type)

            fp.write(self.start_elem("weight"))
            fp.write(self.to_content(edged["weight"]))
            fp.write(self.end_elem("weight"))

            fp.write(self.start_elem("haps_id"))
            for hid in edged["haps_id"]:
                fp.write(self.start_elem("hap_id"))
                fp.write(self.to_content(hid))
                fp.write(self.end_elem("hap_id"))
            fp.write(self.end_elem("haps_id"))
            fp.write(self.end_elem("edge"))
        fp.write(self.end_elem("edges"))

        fp.write(self.end_elem("network"))

        if stream is None:
            return fp.getvalue()

    def load(self, nw, stream, **kwargs):
        pass


#===============================================================================
# MAIN
#===============================================================================

if __name__ == '__main__':
    print(__doc__)

