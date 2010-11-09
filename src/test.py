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
# DOCS
#===============================================================================

"""Yatel Tests"""

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

import unittest
import StringIO
import os

from Bio import Alphabet
from Bio import SeqRecord
from Bio import Seq

from yatel import Network
from yatel import Distance
from yatel import NetworkInfo
from yatel import NetworkIO
from yatel import DB


#===============================================================================
# CONSTANTS
#===============================================================================

_TEST_DATA = _PATH = os.path.abspath(os.path.dirname(__file__)) + \
            os.path.sep + "test_data" + os.path.sep


_SEQS = ["111", "222", "333", "444", "555", "666", "777", "888", "999"]


#===============================================================================
# NETWORK TESTS
#===============================================================================

class NetworkTest(unittest.TestCase):
    
    def setUp(self):
        self.sqrs = []
        self.nwa = Network.Network("test", Alphabet.Alphabet(),
                                  Distance.DefaultDistance())
        for i, s in enumerate(_SEQS):
            seq = Seq.Seq(s) 
            seqr = SeqRecord.SeqRecord(seq=seq, id=str(i), name=s, description=s)
            self.sqrs.append(seqr)
            self.nwa.add(seqr)

        
        
    def test_getitem(self):
        for s in self.sqrs:
            self.assertTrue(self.nwa[s] != None)
        try:
            self.nwa["000"]
        except KeyError:
            pass
        else:
            self.fail("000 do not exist")
            
    def test_len(self):
        self.assertEqual(len(self.nwa), len(_SEQS))


#===============================================================================
# NETWORK INFO TESTS
#===============================================================================

class NetworkInfoTest(unittest.TestCase):

    def setUp(self):
        self.sqrs = []
        self.nwa = Network.Network("test2", Alphabet.Alphabet(),
                                  Distance.DefaultDistance())
        for i, s in enumerate(_SEQS):
            seq = Seq.Seq(s) 
            seqr = SeqRecord.SeqRecord(seq=seq, id=str(i), name=s, description=s)
            self.sqrs.append(seqr)
            self.nwa.add(seqr)
        self.ni = NetworkInfo.NetworkInfo(self.nwa)
    
    def test_distance_anti_mode(self):
        self.ni.distance_anti_mode

    def test_distance_avg(self):
        self.ni.distance_avg

    def test_distance_frequency(self):
        self.ni.distance_frequency

    def test_distance_max(self):
        self.ni.distance_max

    def test_distance_min(self):
        self.ni.distance_min

    def test_distance_mode(self):
        self.ni.distance_mode

    def test_distance_std(self):
        self.ni.distance_std

    def test_distances(self):
        self.ni.distances

    def test_network(self):
        self.ni.network


#===============================================================================
# NETWORK IO TESTS
#===============================================================================

class NetworkIOTest(unittest.TestCase):
    
    def setUp(self):
        # only work with nwa and nwb or nwb with nwc
        self.sqrs = []
        self.nwa = Network.Network("test3a", Alphabet.Alphabet(),
                                   Distance.DefaultDistance())
        for i, s in enumerate(_SEQS):
            seq = Seq.Seq(s) 
            seqr = SeqRecord.SeqRecord(seq=seq, id=str(i), name=s, description=s)
            self.sqrs.append(seqr)
            self.nwa.add(seqr)
        self.nwb = Network.Network("test3b", Alphabet.Alphabet(),
                                   Distance.DefaultDistance())
        for i, s in enumerate(_SEQS):
            seq = Seq.Seq(s) 
            seqr = SeqRecord.SeqRecord(seq=seq, id=str(i), name=s, description=s)
            self.sqrs.append(seqr)
            self.nwb.add(seqr)
         
        self.nwc = Network.Network("test3c", Alphabet.Alphabet(),
                                   Distance.DefaultDistance())
        for i, s in enumerate(_SEQS):
            seq = Seq.Seq(s) 
            seqr = SeqRecord.SeqRecord(seq=seq, id=str(i) + "_", name=s, description=s)
            self.sqrs.append(seqr)
            self.nwc.add(seqr)
            
        self.njd_simple_path = _TEST_DATA + "njd_simple.njd"
        self.njd_multiple_path = _TEST_DATA + "njd_multiple.njd"         
         
    def test_write(self):
        non = NetworkIO.write([self.nwa], StringIO.StringIO(), "njd")
        self.assertEqual(non, 1)
        non = NetworkIO.write([self.nwb], StringIO.StringIO(), "njd")
        self.assertEqual(non, 1)
        non = NetworkIO.write([self.nwc], StringIO.StringIO(), "njd")
        self.assertEqual(non, 1)
        non = NetworkIO.write([self.nwa, self.nwc], StringIO.StringIO(), "njd")
        self.assertEqual(non, 2)
        non = NetworkIO.write([self.nwb, self.nwc], StringIO.StringIO(), "njd")
        self.assertEqual(non, 2)
        try:
            NetworkIO.write([self.nwa, self.nwb], StringIO.StringIO(), "njd")
        except NetworkIO.NetworkFileHandlerError:
            pass
        else:
            self.fail("2 id for siferent SeqRecrods")
        try:
            NetworkIO.write([self.nwa, self.nwa], StringIO.StringIO(), "njd")
        except NetworkIO.NetworkFileHandlerError:
            pass
        else:
            self.fail("2 Networks with same id")
            
    def test_parse(self):
        count = None
        for c, nw in enumerate(NetworkIO.parse(open(self.njd_simple_path, "r"), "njd")):
            self.assertTrue(isinstance(nw, Network.Network))
            count = c
        self.assertEqual(count + 1, 1)
        count = None
        for c, nw in enumerate(NetworkIO.parse(open(self.njd_multiple_path, "r"), "njd")):
            self.assertTrue(isinstance(nw, Network.Network))
            count = c
        self.assertEqual(count + 1, 2)

    def test_read(self):
        nw = NetworkIO.read(open(self.njd_simple_path, "r"), "njd")
        self.assertTrue(isinstance(nw, Network.Network))
        try:
            NetworkIO.read(open(self.njd_multiple_path, "r"), "njd")
        except NetworkIO.NetworkFileHandlerError:
            pass
        else:
            self.fail("method read return more than one Network")
            
#===============================================================================
# TEST DB
#===============================================================================
class NetworkDB(unittest.TestCase):
    
    def setUp(self):
        # only work with nwa and nwb or nwb with nwc
        self.sqrs = []
        self.nwa = Network.Network("test3a", Alphabet.Alphabet(),
                                   Distance.DefaultDistance())
        for i, s in enumerate(_SEQS):
            seq = Seq.Seq(s) 
            seqr = SeqRecord.SeqRecord(seq=seq, id=str(i), name=s, description=s)
            self.sqrs.append(seqr)
            self.nwa.add(seqr)
        self.nwb = Network.Network("test3b", Alphabet.Alphabet(),
                                   Distance.DefaultDistance())
        for i, s in enumerate(_SEQS):
            i += len(self.nwa) 
            seq = Seq.Seq(s) 
            seqr = SeqRecord.SeqRecord(seq=seq, id=str(i), name=s, description=s)
            self.sqrs.append(seqr)
            self.nwb.add(seqr)
         
        self.nwc = Network.Network("test3c", Alphabet.Alphabet(),
                                   Distance.DefaultDistance())
        for i, s in enumerate(_SEQS):
            i += len(self.nwa) + len(self.nwb)
            seq = Seq.Seq(s) 
            seqr = SeqRecord.SeqRecord(seq=seq, id=str(i), name=s, description=s)
            self.sqrs.append(seqr)
            self.nwc.add(seqr)
        DB.connect("memory", create=True, echo=True)
    
    def tearDown(self):
        DB.close()
    
    def test_write(self):
        DB.write(self.nwa)
        
#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    unittest.main()


