import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("cast.c")
    with open("cast.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("cast.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    check50.run("./cast")\
            .stdout("[1, 2, 3]")\
            .stdout("[a, b]")\
            .stdout("[2.500000, 1.100000, 12.420000]")\
            .exit()
