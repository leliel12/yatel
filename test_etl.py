#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''auto created template for create your custom etl for yatel'''


from yatel import etl


#===============================================================================
# PUT YOUT ETLs HERE
#===============================================================================

class CustomETL(etl.ETL):

    def haplotype_gen(self):
        raise NotImplementedError()

    def edge_gen(self):
        raise NotImplementedError()

    def fact_gen(self):
        raise NotImplementedError()

    def get_mode(self):
        raise NotImplementedError()


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)