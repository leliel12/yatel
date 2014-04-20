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

    def test_help(self):
        orig = list(functions.FUNCTIONS.keys())
        rs = self.execute("help")
        self.assertSameUnsortedContent(orig, rs)
        for fname, fdata in functions.FUNCTIONS.items():
            orig = functions.pformat_data(fname)
            rs = self.execute("help", fname=fname)
            self.assertEquals(orig, rs)


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

    def test_sort(self):
        iterable = [idx for idx in self.rrange(1, 100)]
        orig = list(sorted(iterable))
        rs = self.execute("sort", iterable=iterable)
        self.assertEquals(orig, rs)
        orig = list(sorted(iterable, reverse=True))
        rs = self.execute("sort", iterable=iterable, reverse=True)
        self.assertEquals(orig, rs)

        iterable = [
            {"a": random.randint(1, 200)},
            {"a": random.randint(1, 200)}
        ]
        orig = list(sorted(iterable, key=lambda e: e["a"]))
        rs = self.execute("sort", iterable=iterable, key="a")
        self.assertEquals(orig, rs)
        orig = list(sorted(iterable, key=lambda e: e["a"], reverse=True))
        rs = self.execute("sort", iterable=iterable, key="a", reverse=True)
        self.assertEquals(orig, rs)

        dkey = random.randint(1, 300)
        orig = list(sorted(iterable, key=lambda e: dkey))
        rs = self.execute("sort", iterable=iterable, key="b", dkey=dkey)
        self.assertEquals(orig, rs)

        Mock = collections.namedtuple("Mock", ["x"])
        iterable = [
            Mock(x=random.randint(1, 800)), Mock(x=random.randint(1, 800))
        ]
        orig = list(sorted(iterable, key=lambda e: e.x))
        rs = self.execute("sort", iterable=iterable, key="x")
        self.assertEquals(orig, rs)
        orig = list(sorted(iterable, key=lambda e: e.x, reverse=True))
        rs = self.execute("sort", iterable=iterable, key="x", reverse=True)
        self.assertEquals(orig, rs)

        dkey = random.randint(1, 300)
        orig = list(sorted(iterable, key=lambda e: dkey))
        rs = self.execute("sort", iterable=iterable, key="b", dkey=dkey)
        self.assertEquals(orig, rs)

        orig = list(sorted(iterable, key=lambda e: dkey, reverse=True))
        rs = self.execute(
            "sort", iterable=iterable, key="b", dkey=dkey, reverse=True
        )
        self.assertEquals(orig, rs)

    def test_index(self):
        iterable = list(set(idx for idx in self.rrange(100, 200)))
        random.shuffle(iterable)

        orig = len(iterable) / 2
        elem = iterable[orig]

        rs = self.execute("index", iterable=iterable, value=elem)
        self.assertEqual(orig, rs)

        rs = self.execute("index", iterable=iterable, value=elem, start=orig-1)
        self.assertEqual(orig, rs)
        rs = self.execute("index", iterable=iterable, value=elem, start=orig+1)
        self.assertEqual(-1, rs)

        rs = self.execute(
            "index", iterable=iterable, value=elem, start=orig-1, end=orig+1
        )
        self.assertEqual(orig, rs)
        rs = self.execute(
            "index", iterable=iterable, value=elem, start=orig-2, end=orig-1
        )
        self.assertEqual(-1, rs)

    def test_split(self):
        string_s = (
            hashlib.sha512(str(random.random())).hexdigest(),
            hashlib.sha512(str(random.random())).hexdigest(),
            hashlib.sha512(str(random.random())).hexdigest()
        )
        joiners = (
            " ", hashlib.sha512(str(random.random())).hexdigest()
        )
        for joiner in joiners:
            string = joiner.join(string_s)
            orig = string.split(joiner)
            rs = self.execute("split", string=string, s=joiner)
            self.assertEquals(orig, rs)
            orig = string.split(joiner, 1)
            rs = self.execute("split", string=string, s=joiner, maxsplit=1)
            self.assertEquals(orig, rs)

    def test_rsplit(self):
        string_s = (
            hashlib.sha512(str(random.random())).hexdigest(),
            hashlib.sha512(str(random.random())).hexdigest(),
            hashlib.sha512(str(random.random())).hexdigest()
        )
        joiners = (
            " ", hashlib.sha512(str(random.random())).hexdigest()
        )
        for joiner in joiners:
            string = joiner.join(string_s)
            orig = string.rsplit(joiner)
            rs = self.execute("rsplit", string=string, s=joiner)
            self.assertEquals(orig, rs)
            orig = string.rsplit(joiner, 1)
            rs = self.execute("rsplit", string=string, s=joiner, maxsplit=1)
            self.assertEquals(orig, rs)

    def test_strip(self):
        string = " !{}! \n\t".format(
            hashlib.sha512(str(random.random())).hexdigest()
        )
        orig = string.strip()
        rs = self.execute("strip", string=string)
        self.assertEquals(orig, rs)
        self.assertFalse(rs.endswith(string[-1]))
        self.assertFalse(rs.startswith(string[0]))

        tostrip = hashlib.sha512(str(random.random())).hexdigest()
        string = "{} !{}! {}".format(
            tostrip, hashlib.sha512(str(random.random())).hexdigest(), tostrip
        )
        orig = string.strip(tostrip)
        rs = self.execute("strip", string=string, chars=tostrip)
        self.assertEquals(orig, rs)
        self.assertFalse(rs.endswith(string[-1]))
        self.assertFalse(rs.startswith(string[0]))

    def test_lstrip(self):
        string = " !{}! \n\t".format(
            hashlib.sha512(str(random.random())).hexdigest()
        )
        orig = string.lstrip()
        rs = self.execute("lstrip", string=string)
        self.assertEquals(orig, rs)
        self.assertTrue(rs.endswith(string[-1]))
        self.assertFalse(rs.startswith(string[0]))

        tostrip = hashlib.sha512(str(random.random())).hexdigest()
        string = "{} !{}! {}".format(
            tostrip, hashlib.sha512(str(random.random())).hexdigest(), tostrip
        )
        orig = string.lstrip(tostrip)
        rs = self.execute("lstrip", string=string, chars=tostrip)
        self.assertEquals(orig, rs)
        self.assertTrue(rs.endswith(string[-1]))
        self.assertFalse(rs.startswith(string[0]))

    def test_rstrip(self):
        string = " !{}! \n\t".format(
            hashlib.sha512(str(random.random())).hexdigest()
        )
        orig = string.rstrip()
        rs = self.execute("rstrip", string=string)
        self.assertEquals(orig, rs)
        self.assertFalse(rs.endswith(string[-1]))
        self.assertTrue(rs.startswith(string[0]))

        tostrip = hashlib.sha512(str(random.random())).hexdigest()
        string = "{} !{}! {}".format(
            tostrip, hashlib.sha512(str(random.random())).hexdigest(), tostrip
        )
        orig = string.rstrip(tostrip)
        rs = self.execute("rstrip", string=string, chars=tostrip)
        self.assertEquals(orig, rs)
        self.assertFalse(rs.endswith(string[-1]))
        self.assertTrue(rs.startswith(string[0]))

    def test_join(self):
        string_s = (
            hashlib.sha512(str(random.random())).hexdigest(),
            hashlib.sha512(str(random.random())).hexdigest(),
            hashlib.sha512(str(random.random())).hexdigest()
        )
        joiner = hashlib.sha512(str(random.random())).hexdigest()
        orig = joiner.join(string_s)
        rs = self.execute("join", joiner=joiner, to_join=string_s)
        self.assertEqual(orig, rs)

    def test_upper(self):
        string = hashlib.sha512(str(random.random())).hexdigest() + "zzz"
        orig = string.upper()
        rs = self.execute("upper", string=string)
        self.assertEqual(orig, rs)

    def test_lower(self):
        string = hashlib.sha512(str(random.random())).hexdigest() + "QQQ"
        orig = string.lower()
        rs = self.execute("lower", string=string)
        self.assertEqual(orig, rs)

    def test_title(self):
        string = "t" + hashlib.sha512(str(random.random())).hexdigest() + " QQ"
        orig = string.title()
        rs = self.execute("title", string=string)
        self.assertEqual(orig, rs)
        self.assertTrue(rs[0].isupper())
        self.assertTrue(rs[-2].isupper())
        self.assertFalse(rs[-1].isupper())

    def test_capitalize(self):
        string = "t" + hashlib.sha512(str(random.random())).hexdigest() + " QQ"
        orig = string.capitalize()
        rs = self.execute("capitalize", string=string)
        self.assertEqual(orig, rs)
        self.assertTrue(rs[0].isupper())
        self.assertFalse(rs[-2].isupper())
        self.assertFalse(rs[-1].isupper())

    def test_isalnum(self):
        cases = (
            hashlib.sha512(str(random.random())).hexdigest(),
            str(random.randint(100, 1000)), "dhfuoucDSADFDSFsldfnkljsdfb", "!"
        )
        for case in cases:
            orig = case.isalnum()
            rs = self.execute("isalnum", string=case)
            self.assertEqual(orig, rs)

    def test_isalpha(self):
        cases = (
            hashlib.sha512(str(random.random())).hexdigest(),
            str(random.randint(100, 1000)), "dhfuoucDSADFDSFsldfnkljsdfb", "!"
        )
        for case in cases:
            orig = case.isalpha()
            rs = self.execute("isalpha", string=case)
            self.assertEqual(orig, rs)

    def test_isdigit(self):
        cases = (
            hashlib.sha512(str(random.random())).hexdigest(),
            str(random.randint(100, 1000)), "dhfuoucDSADFDSFsldfnkljsdfb", "!"
        )
        for case in cases:
            orig = case.isdigit()
            rs = self.execute("isdigit", string=case)
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
