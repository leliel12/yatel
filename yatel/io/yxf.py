#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 'THE WISKEY-WARE LICENSE':
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

'''Persist yatel db in XML format

'''

#===============================================================================
# IMPORTS
#===============================================================================

from xml import sax
from xml.sax import saxutils

from yatel import typeconv
from yatel.io import core


#===============================================================================
# IO FUNCTIONS
#===============================================================================

class XMLParser(core.BaseParser):

    @classmethod
    def file_exts(cls):
        return ("yxf", "xml")

    #===========================================================================
    # DUMP
    #===========================================================================

    def start_elem(self, tag, attrs={}):
        attrs = u' '.join([u'{}={}'.format(k, saxutils.quoteattr(v))
                                           for k, v in attrs.items()])
        return u'<{tag} {attrs}>'.format(tag=tag, attrs=attrs)

    def end_elem(self, tag):
        return u'</{tag}>'.format(tag=tag)

    def to_content(self, data):
        return saxutils.escape(str(data))


    def dump(self, nw, fp, *args, **kwargs):

        fp.write(self.start_elem(u"Network", {u"version": self.version()}))

        fp.write(self.start_elem(u"Haplotypes"))
        for hap in nw.haplotypes():
            fp.write(self.start_elem(u"Haplotype"))
            for aname, adata in typeconv.simplifier(hap)["value"].items():
                xmlattrs = {u"name": aname, u"type": adata["type"]}
                fp.write(self.start_elem(u"Attribute", xmlattrs))
                fp.write(self.to_content(adata["value"]))
                fp.write(self.end_elem(u"Attribute"))
            fp.write(self.end_elem(u"Haplotype"))
        fp.write(self.end_elem(u"Haplotypes"))

        fp.write(self.start_elem(u"Facts"))
        for fact in nw.facts():
            fp.write(self.start_elem(u"Fact"))
            for aname, adata in typeconv.simplifier(fact)["value"].items():
                xmlattrs = {u"name": aname, u"type": adata["type"]}
                fp.write(self.start_elem(u"Attribute", xmlattrs))
                fp.write(self.to_content(adata["value"]))
                fp.write(self.end_elem(u"Attribute"))
            fp.write(self.end_elem(u"Fact"))
        fp.write(self.end_elem(u"Facts"))

        fp.write(self.start_elem(u"Edges"))
        for edge in nw.edges():
            fp.write(self.start_elem(u"Edge"))
            attrs = typeconv.simplifier(edge)["value"]

            xmlattrs = {u"name": "weight", u"type": attrs["weight"]["type"]}
            fp.write(self.start_elem(u"Attribute", xmlattrs))
            fp.write(self.to_content(attrs["weight"]["value"]))
            fp.write(self.end_elem(u"Attribute"))

            fp.write(self.start_elem(u"Attribute", {u"name": u"haps_id"}))
            for hap_id_data in attrs["haps_id"]["value"]:
                xmlattrs = {"name": u"hap_id", u"type": hap_id_data["type"]}
                fp.write(self.start_elem(u"Attribute", xmlattrs))
                fp.write(self.to_content(hap_id_data["value"]))
                fp.write(self.end_elem(u"Attribute"))
            fp.write(self.end_elem(u"Attribute"))
            fp.write(self.end_elem(u"Edge"))
        fp.write(self.end_elem(u"Edges"))


        fp.write(self.end_elem(u"Network"))


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

