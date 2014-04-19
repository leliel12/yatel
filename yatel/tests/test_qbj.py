#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

#==============================================================================
# DOC
#==============================================================================

"""yatel.qbj package tests"""


#==============================================================================
# IMPORTS
#==============================================================================

import hashlib, random, datetime, collections

from yatel import stats
from yatel.qbj import functions

from yatel.tests.core import YatelTestCase


#==============================================================================
# FUNCTION_TESTS
#==============================================================================

class FunctionTest(YatelTestCase):

    _tested = set()

    @classmethod
    def tearDownClass(cls):
        for k in functions.FUNCTIONS.keys():
            if k not in cls._tested:
                msg = "Please test QBJFunction '{}'".format(k)
                raise AssertionError(msg)

    def execute(self, name, nw=None, *args, **kwargs):
        self._tested.add(name)
        nw = self.nw if nw is None else nw
        return functions.execute(name, nw, *args, **kwargs)

    def test_haplotypes(self):
        orig = tuple(self.nw.haplotypes())
        rs = tuple(self.execute("haplotypes"))
        self.assertSameUnsortedContent(rs, orig)

    def test_haplotype_by_id(self):
        orig = self.rchoice(self.nw.haplotypes())
        rs = self.execute("haplotype_by_id", hap_id=orig.hap_id)
        self.assertEqual(rs, orig)

    def test_haplotypes_by_enviroment(self):
        for env in list(self.nw.enviroments()) + [None]:
            orig = tuple(self.nw.haplotypes_by_enviroment(env))
            rs = tuple(self.execute("haplotypes_by_enviroment", env=env))
            self.assertSameUnsortedContent(rs, orig)

    def test_edges(self):
        orig = tuple(self.nw.edges())
        rs = tuple(self.execute("edges"))
        self.assertSameUnsortedContent(rs, orig)

    def test_edges_by_haplotype(self):
        hap = self.rchoice(self.nw.haplotypes())
        orig = tuple(self.nw.edges_by_haplotype(hap))
        rs = tuple(self.execute("edges_by_haplotype", hap=hap))
        self.assertEqual(rs, orig)

    def test_edges_by_enviroment(self):
        for env in list(self.nw.enviroments()) + [None]:
            orig = tuple(self.nw.edges_by_enviroment(env))
            rs = tuple(self.execute("edges_by_enviroment", env=env))
            self.assertSameUnsortedContent(rs, orig)

    def test_facts(self):
        orig = tuple(self.nw.facts())
        rs = tuple(self.execute("facts"))
        self.assertSameUnsortedContent(rs, orig)

    def test_facts_by_haplotype(self):
        hap = self.rchoice(self.nw.haplotypes())
        orig = tuple(self.nw.facts_by_haplotype(hap))
        rs = tuple(self.execute("facts_by_haplotype", hap=hap))
        self.assertEqual(rs, orig)

    def test_facts_by_enviroment(self):
        for env in list(self.nw.enviroments()) + [None]:
            orig = tuple(self.nw.facts_by_enviroment(env))
            rs = tuple(self.execute("facts_by_enviroment", env=env))
            self.assertSameUnsortedContent(rs, orig)

    def test_describe(self):
        orig = self.nw.describe()
        rs = self.execute("describe")
        self.assertEqual(rs, orig)

    def test_enviroments(self):
        orig = tuple(self.nw.enviroments())
        rs = tuple(self.execute("enviroments"))
        self.assertSameUnsortedContent(rs, orig)

    def test_env2weightarray(self):
        for env in list(self.nw.enviroments()) + [None]:
            orig = list(stats.env2weightarray(self.nw, env))
            rs = list(self.execute("env2weightarray", env=env))
            self.assertEqual(orig, rs)

    def test_min(self):
        for env in list(self.nw.enviroments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.min(self.nw, env)
                rs_nw = self.execute("min", env=env)
                orig_arr = stats.min(arr)
                rs_arr = self.execute("min", nw=arr)
                self.assertTrue(
                    orig_nw == rs_nw and rs_nw == orig_arr and
                    orig_arr == rs_arr and rs_arr == orig_nw
                )

    def test_sum(self):
        for env in list(self.nw.enviroments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.sum(self.nw, env)
                rs_nw = self.execute("sum", env=env)
                orig_arr = stats.sum(arr)
                rs_arr = self.execute("sum", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_var(self):
        for env in list(self.nw.enviroments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.var(self.nw, env)
                rs_nw = self.execute("var", env=env)
                orig_arr = stats.var(arr)
                rs_arr = self.execute("var", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_mode(self):
        for env in list(self.nw.enviroments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = list(stats.mode(self.nw, env))
                rs_nw = list(self.execute("mode", env=env))
                orig_arr = list(stats.mode(arr))
                rs_arr = list(self.execute("mode", nw=arr))
                self.assertEqual(orig_nw, rs_nw)
                self.assertEqual(orig_arr, rs_arr)
                self.assertEqual(orig_nw, orig_arr)

    def test_max(self):
        for env in list(self.nw.enviroments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.max(self.nw, env)
                rs_nw = self.execute("max", env=env)
                orig_arr = stats.max(arr)
                rs_arr = self.execute("max", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_variation(self):
        for env in list(self.nw.enviroments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.variation(self.nw, env=env)
                rs_nw = self.execute("variation", env)
                orig_arr = stats.variation(arr)
                rs_arr = self.execute("variation", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_kurtosis(self):
        for env in list(self.nw.enviroments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.kurtosis(self.nw, env)
                rs_nw = self.execute("kurtosis", env=env)
                orig_arr = stats.kurtosis(arr)
                rs_arr = self.execute("kurtosis", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_amax(self):
        for env in list(self.nw.enviroments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.amax(self.nw, env)
                rs_nw = self.execute("amax", env=env)
                orig_arr = stats.amax(arr)
                rs_arr = self.execute("amax", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_std(self):
        for env in list(self.nw.enviroments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.std(self.nw, env)
                rs_nw = self.execute("std", env=env)
                orig_arr = stats.std(arr)
                rs_arr = self.execute("std", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_amin(self):
        for env in list(self.nw.enviroments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.amin(self.nw, env)
                rs_nw = self.execute("amin", env=env)
                orig_arr = stats.amin(arr)
                rs_arr = self.execute("amin", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_average(self):
        for env in list(self.nw.enviroments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.average(self.nw, env)
                rs_nw = self.execute("average", env=env)
                orig_arr = stats.average(arr)
                rs_arr = self.execute("average", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_median(self):
        for env in list(self.nw.enviroments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.median(self.nw, env)
                rs_nw = self.execute("median", env=env)
                orig_arr = stats.median(arr)
                rs_arr = self.execute("median", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_range(self):
        for env in list(self.nw.enviroments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.range(self.nw, env)
                rs_nw = self.execute("range", env=env)
                orig_arr = stats.range(arr)
                rs_arr = self.execute("range", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_percentile(self):
        for env in list(self.nw.enviroments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                for q in range(0, 100):
                    orig_nw = stats.percentile(self.nw, q, env)
                    rs_nw = self.execute("percentile", q=q, env=env)
                    orig_arr = stats.percentile(arr, q)
                    rs_arr = self.execute("percentile", q=q, nw=arr)
                    self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                    self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                    self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_slice(self):
        iterables = [
            list(range(1000)), hashlib.sha512(str(random.random())).hexdigest()
        ]
        for iterable in iterables:
            il = int(len(iterable) - len(iterable) / 3)
            sl  = int(len(iterable) - len(iterable) / 4)
            orig = iterable[il:sl]
            rs = self.execute("slice", iterable=iterable, f=il, t=sl)
            self.assertEqual(orig, rs)

            orig = iterable[il:]
            rs = self.execute("slice", iterable=iterable, f=il)
            self.assertEqual(orig, rs)

    def test_size(self):
        iterable = [idx for idx in self.rrange(1, 1000)]
        orig = len(iterable)
        rs = self.execute("size", iterable=iterable)
        self.assertEqual(orig, rs)

    def test_utcnow(self):
        orig = datetime.datetime.utcnow()
        rs = self.execute("utcnow")
        self.assertAproxDatetime(orig, rs)

    def test_utctime(self):
        orig = datetime.datetime.utcnow().time()
        rs = self.execute("utctime")
        self.assertAproxDatetime(orig, rs)

    def test_utctoday(self):
        orig = datetime.datetime.utcnow().date()
        rs = self.execute("utctoday")
        self.assertAproxDatetime(orig, rs)

    def test_today(self):
        orig = datetime.date.today()
        rs = self.execute("today")
        self.assertAproxDatetime(orig, rs)

    def test_now(self):
        orig = datetime.datetime.now()
        rs = self.execute("now")
        self.assertAproxDatetime(orig, rs)

    def test_time(self):
        orig = datetime.datetime.now().time()
        rs = self.execute("time")
        self.assertAproxDatetime(orig, rs)

    def test_minus(self):
        a = random.randint(100, 1000)
        b = random.randint(100, 1000)
        orig = a - b
        rs = self.execute("minus", minuend=a, sust=b)
        self.assertEqual(orig, rs)

    def test_times(self):
        a = random.randint(100, 1000)
        b = random.randint(100, 1000)
        orig = a * b
        rs = self.execute("times", t0=a, t1=b)
        self.assertEqual(orig, rs)

    def test_div(self):
        a = random.randint(100, 1000)
        b = float(random.randint(100, 1000))
        orig = a / b
        rs = self.execute("div", dividend=a, divider=b)
        self.assertAlmostEqual(orig, rs, places=4)

    def test_floor(self):
        a = random.randint(100, 1000)
        b = float(random.randint(100, 1000))
        orig = a % b
        rs = self.execute("floor", dividend=a, divider=b)
        self.assertAlmostEqual(orig, rs, places=4)

    def test_pow(self):
        a = random.randint(100, 1000)
        b = random.randint(100, 1000)
        orig = a ** b
        rs = self.execute("pow", radix=a, exp=b)
        self.assertAlmostEqual(orig, rs, places=4)

    def test_xroot(self):
        rs = self.execute("xroot", radix=8, root=3)
        self.assertAlmostEqual(2, rs, places=4)

    def test_count(self):
        iterable = [idx for idx in self.rrange(1, 100)]
        counter = collections.Counter(iterable)
        for elem, orig in counter.items():
            rs = self.execute("count", iterable=iterable, to_count=elem)
            self.assertEqual(orig, rs)


#==============================================================================
# QBJ
#==============================================================================

#~ class QBJEngineTest(YatelTestCase):
#~
    #~ def setUp(self):
        #~ super(QBJEngineTest, self).setUp()
        #~ self.jnw = qbj.QBJEngine(self.nw)
#~
    #~ def test_valid_queries(self):
        #~ for dictionary in queries.VALID:
            #~ string = json.dumps(dictionary)
            #~ stream = StringIO.StringIO(string)
            #~ for q in [dictionary, string, stream]:
                #~ result = self.jnw.execute(q, True)
                #~ if result["error"]:
                    #~ self.fail("\n".join(
                        #~ [result["error_msg"], result["stack_trace"]])
                    #~ )


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
