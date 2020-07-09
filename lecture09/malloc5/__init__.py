import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("malloc5.c")
    with open("malloc5.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("malloc5.c", cc="gcc")

@check50.check(exists)
def validate(sources_buf):
    if "malloc" not in sources_buf:
        raise check50.Failure("Cannot find call to malloc")
    if "free" not in sources_buf:
        raise check50.Failure("Cannot find a call to free")

@check50.check(compiles)
def output_correct():
    check50.run("./malloc5")\
        .stdout("0 2 4 6 8 10 12 14 16 18")\
        .exit()

@check50.check(compiles)
def valgrind_memcheck():
    check50.c.valgrind("./malloc5").exit()

