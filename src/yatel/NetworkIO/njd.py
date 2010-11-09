#!/usr/bin/env python
#-*-coding:utf-8-*-

# Copyright (C) 2010 Juan BC <jbc dot develop at gmail dot com>

# Biopython License Agreement

# Permission to use, copy, modify, and distribute this software and its
# documentation with or without modifications and for any purpose and
# without fee is hereby granted, provided that any copyright notices
# appear in all copies and that both those copyright notices and this
# permission notice appear in supporting documentation, and that the
# names of the contributors or copyright holders not be used in
# advertising or publicity pertaining to distribution of the software
# without specific prior permission.

# THE CONTRIBUTORS AND COPYRIGHT HOLDERS OF THIS SOFTWARE DISCLAIM ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL THE
# CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY SPECIAL, INDIRECT
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE
# OR PERFORMANCE OF THIS SOFTWARE.

#===============================================================================
# FUTURE
#===============================================================================

from __future__ import absolute_import

#===============================================================================
# DOCS
#===============================================================================

"""File parser for njd (Network json definition)"""


#===============================================================================
# META
#===============================================================================

__version__ = "0.1"
__license__ = "Biopython License"
__author__ = "JBC <jbc dot develop at gmail dot com>"
__since__ = "0.1"
__date__ = "2010-08-04"


#===============================================================================
# IMPORTS
#===============================================================================

import json

from Bio import Seq
from Bio import SeqRecord
from Bio import Alphabet

from yatel import Distance
from yatel import Network

from yatel.NetworkIO import base


#===============================================================================
# CLASSES
#===============================================================================

class NJDError(base.NetworkFileHandlerError):
    pass


class NJDFileHandler(base.AbstractNetworkFileHandler):
        
    def parse(self, handle):
        data = json.load(handle) 
        seqs_r = {} 
        for id, seq_data in data["sequences"].items():
            id = str(id)
            if id not in seqs_r:
                seq_r = SeqRecord.SeqRecord(id=id,
                                            seq=Seq.Seq(seq_data["seq"]),
                                            name=seq_data["name"],
                                            description=seq_data["description"],
                                            dbxrefs=seq_data["dbxrefs"],
                                            annotations=seq_data["annotations"],
                                            letter_annotations=seq_data["letter_annotations"])
            else:
                msg = "Duplicated SeqRecord ID '%s'" % id
                raise NJDError(msg)
            seqs_r[id] = seq_r
        
        for nw_id, nw_data in data["networks"].items():
            distance = Distance.ExpertDistance()
            seqs = set()
            for id0, id1, d in nw_data["relations"]:
                seq_r0 = seqs_r[id0]
                seq_r1 = seqs_r[id1]
                seqs.add(seq_r0)
                seqs.add(seq_r1)
                distance.add_distance(seq_r0, seq_r1, float(d))   
            yield Network.Network(id=nw_id,
                                  alphabet=Alphabet.Alphabet(),
                                  distance=distance,
                                  name=nw_data["name"],
                                  description=nw_data["description"],
                                  annotations=nw_data["annotations"],
                                  sequences=seqs)

        
    def write(self, networks, handle):
        sequence_dicts = {}
        network_dicts = {}
        
        for nw in networks:
            
            if nw.id in network_dicts:
                msg = "Duplicated Network ID '%s'" % str(nw.id)
                raise NJDError(msg)
            
            nw_dict = {}
            nw_dict["name"] = nw.name
            nw_dict["description"] = nw.description
            nw_dict["annotations"] = nw.annotations
            nw_dict["relations"] = []
            
            for seqr, distances in nw.items():
                
                if seqr.id in sequence_dicts:
                    msg = "Duplicated SeqRecord ID '%s'" % str(seqr.id)
                    raise NJDError(msg)
                
                seq_dict = {}
                seq_dict["seq"] = str(seqr.seq)
                seq_dict["name"] = seqr.name or ""
                seq_dict["description"] = seqr.description or ""
                seq_dict["annotations"] = seqr.annotations or {}
                seq_dict["letter_annotations"] = seqr.letter_annotations or {}
                seq_dict["dbxrefs"] = seqr.dbxrefs or []
                sequence_dicts[seqr.id] = seq_dict
                
                for to, d in distances.items():
                    if d != None:
                        nw_dict["relations"].append((seqr.id, to.id, d))

                    
            network_dicts[nw.id] = nw_dict
        
        data = {"sequences":sequence_dicts, "networks": network_dicts}
        json.dump(data, handle, indent=True)
        return len(network_dicts)

            
#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__

