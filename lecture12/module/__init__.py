import check50
import check50.c
import re

srcs = ["main.c", "module1.c", "module1.h", "module2.c", "module2.h",
        "module3.c", "module3.h"]

@check50.check()
def exists():
    sources = {}

    for src in srcs:
        check50.exists(src)
        with open(src) as f:
            sources[src] = f.read()

    return sources

@check50.check(exists)
def compiles():
    check50.c.compile("main.c", "module1.c", "module2.c", "module3.c",
            cc="gcc")

@check50.check(exists)
def validate(sources):
    pass

@check50.check(compiles)
def output_correct():
    check50.run("./module")\
            .stdout("module3_function1 called with parameter CASE2")\
            .stdout("res1: 84")\
            .stdout("res2: 1.0+")\
            .stdout("res3: [1-9]+")\
            .exit()

