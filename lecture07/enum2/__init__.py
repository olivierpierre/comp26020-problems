import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("enum.c")
    with open("enum.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("enum.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    check50.run("./enum2")\
            .stdout("f1:")\
            .stdout("FLAG1 enabled")\
            .stdout("FLAG2 enabled")\
            .stdout("f2:")\
            .stdout("FLAG1 enabled")\
            .stdout("FLAG2 enabled")\
            .stdout("FLAG3 enabled")\
            .exit()
