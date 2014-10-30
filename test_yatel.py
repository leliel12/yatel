#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

DBS = [
    "sqlite:///",
    "mysql://root:root@localhost:3306/test_yatel",
    #~ "mysql+oursql://root:root@localhost:3306/test_yatel",

    #~ "postgresql://pg_yatel_test:probando123@web427.webfaction.com:5432/pg_yatel_test",
    #~ "postgresql+psycopg2://pg_yatel_test:probando123@web427.webfaction.com:5432/pg_yatel_test",
    #"postgresql+pg8000://pg_yatel_test:probando123@web427.webfaction.com:5432/pg_yatel_test",
]

YATEL_TEST_DBS = ";".join(DBS)

YATEL = "yatel test 2 "

CMD = "export YATEL_TEST_DBS='{}'; {}".format(YATEL_TEST_DBS, YATEL)

os.system(CMD)

