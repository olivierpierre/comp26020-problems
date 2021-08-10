import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("malloc3.c")
    with open("malloc3.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("malloc3.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    check50.run("./malloc3")\
        .stdout("0 2 4 6 8 10 12 14 16 18")\
        .exit()

@check50.check(compiles)
def valgrind_memcheck():
    check50.c.valgrind("./malloc3").exit()

