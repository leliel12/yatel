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

from xml import sax
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

    #===========================================================================
    # DUMP
    #===========================================================================

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
        hap_types = nw.describe()["haplotype_attributes"]
        fact_types = nw.describe()["fact_attributes"]
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
        for hap in nw.haplotypes():
            fp.write(self.start_elem("haplotype"))
            hapd = self.hap2dict(hap, hap_id_type, hap_types)
            for k, v in hapd.items():
                fp.write(self.start_elem("attribute", {"name": k}))
                fp.write(self.to_content(v))
                fp.write(self.end_elem("attribute"))
            fp.write(self.end_elem("haplotype"))
        fp.write(self.end_elem("haplotypes"))

        fp.write(self.start_elem("facts"))
        for fact in nw.facts():
            fp.write(self.start_elem("fact"))
            factd = self.fact2dict(fact, hap_id_type, fact_types)
            for k, v in factd.items():
                fp.write(self.start_elem("attribute", {"name": k}))
                fp.write(self.to_content(v))
                fp.write(self.end_elem("attribute"))
            fp.write(self.end_elem("fact"))
        fp.write(self.end_elem("facts"))

        fp.write(self.start_elem("edges"))
        for edge in nw.edges():
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

    #===========================================================================
    # LOAD
    #===========================================================================

    def load(self, nw, stream, **kwargs):
        self.validate_write(nw)

        fp = StringIO.StringIO(stream) \
             if isinstance(stream, basestring) \
             else stream

        class YatelXMLHandler(sax.ContentHandler):

            def __init__(self, parent, *args, **kwargs):

                self.hap_types = {}
                self.fact_types = {}
                self.hap_id_type = None
                self.version = None

                self.stk = []
                self.buff = None
                self.parent = parent

            def startElement(self, name, attrs):
                self.stk.append(name.lower())

                # first element
                if self.stk == ["network"]:
                    self.version = saxutils.unescape(attrs["version"])

                # types
                elif self.stk == ["network", "types", "haplotypes", "type"]:
                    name = saxutils.unescape(attrs["name"])
                    self.buff = name
                elif self.stk == ["network", "types", "facts", "type"]:
                    name = saxutils.unescape(attrs["name"])
                    self.buff = name

                # haplotypes
                elif self.stk == ["network", "haplotypes", "haplotype"]:
                    self.buff = {"last": None, "attrs": {}}
                elif self.stk == ["network", "haplotypes", "haplotype", "attribute"]:
                    name = saxutils.unescape(attrs["name"])
                    self.buff["last"] =  name

                # facts
                elif self.stk == ["network", "facts", "fact"]:
                    self.buff = {"last": None, "attrs": {}}
                elif self.stk == ["network", "facts", "fact", "attribute"]:
                    name = saxutils.unescape(attrs["name"])
                    self.buff["last"] =  name

                # edges
                elif self.stk == ["network", "edges", "edge"]:
                    self.buff = {"weight": None, "haps_id": []}

            def characters(self, content):
                content = saxutils.unescape(content)

                # types
                if self.stk == ["network", "types", "haplotypes", "type"]:
                    self.buff = {self.buff: content}
                elif self.stk == ["network", "types", "facts", "type"]:
                    self.buff = {self.buff: content}

                # haplotypes
                elif self.stk == ["network", "haplotypes", "haplotype", "attribute"]:
                    last = self.buff["last"]
                    self.buff["attrs"][last] = content

                # facts
                elif self.stk == ["network", "facts", "fact", "attribute"]:
                    last = self.buff["last"]
                    self.buff["attrs"][last] = content

                # edges
                elif self.stk == ["network", "edges", "edge", "weight"]:
                    self.buff["weight"] = float(content)
                elif self.stk == ["network", "edges", "edge", "haps_id", "hap_id"]:
                    self.buff["haps_id"].append(content)

            def endElement(self, name):
                if self.stk[-1] != name.lower():
                    return

                # types
                if self.stk == ["network", "types", "haplotypes", "type"]:
                    self.hap_types.update(self.buff)
                elif self.stk == ["network", "types", "haplotypes"]:
                    self.hap_types = self.parent.strdict2types(self.hap_types)
                elif self.stk == ["network", "types", "facts", "type"]:
                    self.fact_types.update(self.buff)
                elif self.stk == ["network", "types", "facts"]:
                    self.fact_types = self.parent.strdict2types(self.fact_types)
                elif self.stk == ["network", "types"]:
                    self.hap_id_type = self.hap_types["hap_id"]

                # haplotypes
                elif self.stk == ["network", "haplotypes", "haplotype"]:
                    hapd = self.buff["attrs"]
                    hap = self.parent.dict2hap(hapd,
                                               self.hap_id_type, self.hap_types)
                    nw.add_element(hap)

                # facts
                elif self.stk == ["network", "facts", "fact"]:
                    factd = self.buff["attrs"]
                    fact = self.parent.dict2fact(factd,
                                                 self.hap_id_type,
                                                 self.fact_types)
                    nw.add_element(fact)

                # edges
                elif self.stk == ["network", "edges", "edge"]:
                    edge = self.parent.dict2edge(self.buff, self.hap_id_type)
                    nw.add_element(edge)

                self.stk.pop()

        handler = YatelXMLHandler(self)
        sax.parse(fp, handler)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == '__main__':
    print(__doc__)

