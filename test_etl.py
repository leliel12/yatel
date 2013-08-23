#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''auto created template for create your custom etl for yatel'''

import random

from yatel import dom
from yatel import etl


#===============================================================================
# PUT YOUT ETLs HERE
#===============================================================================

class MyETL(etl.ETL):

    def setup(self, lll, coso):
        import sys
        print lll
        sys.exit(0)
        print "setup :)"
        self.haps_id = []

    def haplotype_gen(self):
        print "haplotype gen!!!"
        for idx in range(10):
            yield dom.Haplotype(idx)
            self.haps_id.append(idx)

    def edge_gen(self):
        buff = set()
        for idx in range(3):
            f, t = random.choice(self.haps_id), random.choice(self.haps_id)
            while (f, t) in buff:
                f, t = random.choice(self.haps_id), random.choice(self.haps_id)
            buff.add((f, t))
            yield dom.Edge(random.randint(1,10), f, t)

    def fact_gen(self):
        print "fact gen!!!"
        for hap_id in self.haps_id:
            yield dom.Fact(hap_id)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
