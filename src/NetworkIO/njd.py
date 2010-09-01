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


################################################################################
# DOCS
################################################################################

"""File parser for njd (Network json definition)"""


################################################################################
# META
################################################################################

__version__ = "0.1"
__license__ = "Biopython License"
__author__ = "JBC <jbc dot develop at gmail dot com>"
__since__ = "0.1"
__date__ = "2010-08-04"


################################################################################
# IMPORTS
################################################################################

import json

from Bio import Seq
from Bio import SeqRecord
from Bio import Alphabet

from Network import Network
from Network import Distance


import base


################################################################################
# CLASSES
################################################################################

src = {
    
    "sequences":
        {
            "1":
                {"seq": "00001", "description": "lalalal"},
            "2":
                {"seq": "11110", "description": "lololol"}
        },
        
    "networks":
        [
            [("1", "2", 3), ("2", "1", 2)],
            [("1", "2", 3), ("2", "1", 2)]
        ]
}

import StringIO

src = StringIO.StringIO(json.dumps(src))

class NJDError(BaseException):
    pass

class NJDFileHandler(base.AbstractNetworkFileHandler):
    
    def read(self, handle):
        ok = True
        for nw in self.parse(handle):
            if ok:
                return nw
            else:
                raise NJDError("More than one network")
        raise StopIteration() 
    
    def parse(self, handle):
        try:
            data = json.load(handle)
            seqs_r = {} 
            for id, seq_data in data["sequences"].items():
                seq = Seq.Seq(seq_data["seq"])
                id = str(id)
                name = seq_data.get("name", "")
                desc = seq_data.get("description", "")
                annt = seq_data.get("annotations", {})
                l_annt = seq_data.get("letter_annotations", {})
                dbxrefs = seq_data.get("dbxrefs", [])
                features = seq_data.get("features", []) 
                seq_r = SeqRecord.SeqRecord(seq=seq,
                                            id=id,
                                            name=name,
                                            description=desc,
                                            dbxrefs=dbxrefs,
                                            features=features,
                                            annotations=annt,
                                            letter_annotations=l_annt)
                seqs_r[id] = seq_r
            for network in data["networks"]:
                distance = Distance.ExpertDistance()
                for id0, id1, d in network:
                    s0 = seqs_r[id0]
                    s1 = seqs_r[id1]
                    try:
                        d = int(d)
                    except ValueError:
                        d = float(d)
                    distance.add_distance(s0, s1, d)
                nw = Network.Network(Alphabet.Alphabet(), distance)
                for sr in seqs_r.values():
                    nw.add(sr)
                yield nw
        except Exception as err:
            raise NJDError(str(err))
        
    def write(self, sequences, handle):
        pass

for nw in NJDFileHandler().parse(src):
    for d in nw.items():
        print d
    import sys
    sys.exit(0)

################################################################################
# MAIN
################################################################################

if __name__ == "__main__":
    print __doc__

